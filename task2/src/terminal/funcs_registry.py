from datetime import datetime
from datetime import timedelta
from sys import exit
import warnings
from typing import Optional

import pandas as pd
import pymongo
import requests

import io
from contextlib import redirect_stdout

from src.mongo.mongo_client import MongoDBClient
from .user import CurrentUser

MONGO_CLIENT = MongoDBClient('clients')
ML_MODEL_URL = 'http://ml_model:8080/predict'

warnings.filterwarnings('ignore')
summary = ''


def get_top_5_users() -> None:
    global summary
    cursor = MONGO_CLIENT.db.sessions.find(
        {}, {'client_user_id': 1, 'session_id': 1, 'timestamp': 1, '_id': 0}
    )
    df = pd.DataFrame(list(cursor))
    df.loc[:, 'timestamp'] = df.timestamp.astype('datetime64[ns]')

    df_grouped = df.groupby(['client_user_id', 'session_id'])
    session_times = (df_grouped.timestamp.max() - df_grouped.timestamp.min()).reset_index().drop('session_id', axis=1)
    client_times = session_times.groupby('client_user_id').sum()
    top_5_users = client_times.sort_values(by='timestamp', ascending=False).head(5)

    with io.StringIO() as buffer, redirect_stdout(buffer):
        print('Top 5 clients based on game time:')
        [print(f'\t{user} – {time}') for user, time in zip(top_5_users.index, top_5_users.timestamp)]
        summary = buffer.getvalue()

    print(summary)


def get_7_days_status() -> None:
    global summary
    last_week_results_df = _get_data_for_last_7_days()

    with io.StringIO() as buffer, redirect_stdout(buffer):
        print(f'\tTotal sessions: {len(last_week_results_df.session_id.value_counts())}')
        print(f'\tMean t. / session: {_get_average_time_per_session(last_week_results_df).total_seconds() // 60} min.')
        print(f'\tSum of hours spent by all users: {_get_total_hours_for_last_7_days(last_week_results_df)} hours')
        summary = buffer.getvalue()

    print(summary)


def predict_session_duration() -> None:
    user_id = CurrentUser().user_id
    results_df = pd.DataFrame(
        list(MONGO_CLIENT.db.sessions.find({'client_user_id': user_id}))
    )

    print(f'\tEstimated next session time: {_get_previous_session_time(results_df)}\n')


def get_bad_sessions_count(features: pd.DataFrame) -> str:
    return requests.post(ML_MODEL_URL, json=features.to_dict()).text


def save_to_txt() -> None:
    with open('summary.txt', 'w') as f:
        f.write(summary)


def exit_program() -> None:
    exit()


def print_summary() -> None:
    global summary
    end_date, start_date, user_id = _get_date_and_user_id()
    results_df = _get_data_from_mongo(end_date, start_date, user_id)

    with io.StringIO() as buffer, redirect_stdout(buffer):
        if results_df is not None:
            print(f'\tNumber of sessions: {len(results_df.session_id.value_counts())}')
            print(f'\tDate of first session: {results_df.timestamp.iloc[0]}')
            print(f'\tAverage time spent per session: {_get_average_time_per_session(results_df)}')
            print(f'\tDate of most recent session: {results_df.timestamp.iloc[-1]}')
            print(f'\tMost used device: {results_df.device.value_counts().sort_values(ascending=False).index[0]}')
            print(f'\tTotal number of bad sessions: {_get_bad_sessions_count(results_df)}')
            print(f'\tDevices used: {results_df.device.unique()}')
            print(f'\tEstimated next session time: {_get_previous_session_time(results_df)}')
            print(f'\tSuper user: {_is_super_user(end_date, start_date, results_df)}\n')
        else:
            print('User not found!\n')

        summary = buffer.getvalue()

    print(summary)


def enter_user_id() -> None:
    CurrentUser().user_id = input()
    if CurrentUser().user_id:
        pass
    else:
        CurrentUser().user_id = "abc"


def enter_period() -> None:
    CurrentUser().period = input()


def _get_data_for_last_7_days() -> pd.DataFrame:
    end_date_str = list(MONGO_CLIENT.db.sessions.find().sort([('_id', pymongo.DESCENDING)]).limit(1))[0]['timestamp']
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    week_ago_date = end_date - timedelta(days=7)
    cursor = MONGO_CLIENT.db.sessions.find(
        {'timestamp': {'$gt': str(week_ago_date)}}, {'client_user_id': 1, 'session_id': 1, 'timestamp': 1, '_id': 0}
    )
    last_week_results_df = pd.DataFrame(list(cursor))
    last_week_results_df.loc[:, 'timestamp'] = last_week_results_df.timestamp.astype('datetime64[ns]')
    return last_week_results_df


def _get_total_hours_for_last_7_days(last_week_results_df: pd.DataFrame) -> float:
    df_grouped = last_week_results_df.groupby(['client_user_id', 'session_id'])
    return (df_grouped.max() - df_grouped.min()).sum()[0].total_seconds() // 3600


def _get_previous_session_time(results_df: pd.DataFrame) -> float:
    results_df.loc[:, 'timestamp'] = results_df.timestamp.astype('datetime64[ns]')
    return (results_df.groupby('session_id').timestamp.max() - results_df.groupby('session_id').timestamp.min())[-1]


def _get_average_time_per_session(results_df: pd.DataFrame) -> float:
    return (results_df.groupby('session_id').timestamp.max() - results_df.groupby('session_id').timestamp.min()).mean()


def _is_super_user(end_date: datetime, start_date: datetime, results_df: pd.DataFrame) -> bool:
    week_ago = end_date - timedelta(days=7)
    week_ago_date = start_date if start_date > week_ago else week_ago
    results_week_df = results_df[(results_df.timestamp >= week_ago_date) & (results_df.timestamp <= end_date)]
    super_user = False
    if (
        results_week_df.groupby('session_id').timestamp.max() - results_week_df.groupby('session_id').timestamp.min()
    ).sum() > timedelta(minutes=60):
        super_user = True
    return super_user


def _get_date_and_user_id() -> (datetime, datetime, str):
    period = CurrentUser().period
    start_date = datetime.strptime(period.split(' ')[0], '%Y-%m-%d')
    end_date = datetime.strptime(period.split(' ')[1], '%Y-%m-%d')
    user_id = CurrentUser().user_id
    return end_date, start_date, user_id


def _get_data_from_mongo(end_date: datetime, start_date: datetime, user_id: str) -> Optional[pd.DataFrame]:
    results_df = pd.DataFrame(
        list(MONGO_CLIENT.db.sessions.find({'client_user_id': user_id}))
    )
    results_df.loc[:, 'timestamp'] = results_df.timestamp.astype('datetime64[ns]')

    return (
        results_df[(results_df.timestamp >= start_date) & (results_df.timestamp <= end_date)]
        if len(results_df) else None
    )


def _get_bad_sessions_count(results_df: pd.DataFrame) -> float:
    stds = results_df.groupby('session_id').std()[['FPS', 'RTT']].rename(columns={'FPS': 'fps_std', 'RTT': 'rtt_std'})
    means = results_df.groupby('session_id').mean()[['FPS', 'RTT']].rename(
        columns={'FPS': 'fps_mean', 'RTT': 'rtt_mean'}
    )
    columns_right_order = ['fps_mean', 'fps_std', 'rtt_mean', 'rtt_std']
    features = stds.join(means).loc[:, columns_right_order]
    sessions_quality = get_bad_sessions_count(features)

    return sessions_quality.count('false')
