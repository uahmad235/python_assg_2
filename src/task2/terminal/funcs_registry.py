from datetime import datetime
from datetime import timedelta
from sys import exit
import warnings
from typing import Optional

import pandas as pd
import requests

from src.task2.mongo.mongo_client import MongoDBClient
from .user import CurrentUser

MONGO_CLIENT = MongoDBClient('clients')
ML_MODEL_URL = 'http://127.0.0.1:8080/predict'

warnings.filterwarnings('ignore')


def get_top_5_users() -> None:
    print('Top 5 users')


def get_7_days_status() -> None:
    print('7 days status')


def predict_session_duration(features) -> str:
    query_params = {
        'dropped_frames': 1,
        'FPS': 1
    }

    prediction = requests.post(ML_MODEL_URL, json=query_params)
    return prediction.text


def save_to_txt() -> None:
    print('Saved to txt')


def exit_program() -> None:
    exit()


def print_summary() -> None:
    end_date, start_date, user_id = _get_date_and_user_id()
    results_df = _get_data_from_mongo(end_date, start_date, user_id)

    if results_df is not None:
        print(f'\tNumber of sessions: {len(results_df.session_id.value_counts())}')
        print(f'\tDate of first session: {results_df.timestamp.iloc[0]}')
        print(f'\tAverage time spent per session: {_get_average_time_per_session(results_df)}')
        print(f'\tDate of most recent session: {results_df.timestamp.iloc[-1]}')
        print(f'\tMost used device: {results_df.device.value_counts().sort_values(ascending=False).index[0]}')
        print(f'\tDevices used: {results_df.device.unique()}')
        print(f'\tEstimated next session time: {_get_previous_session_time(results_df)}')
        print(f'\tSuper user: {_is_super_user(end_date, start_date, results_df)}')
    else:
        print('User not found!')


def enter_user_id() -> None:
    CurrentUser().user_id = input()


def enter_period() -> None:
    CurrentUser().period = input()


def _get_previous_session_time(results_df) -> float:
    return (results_df.groupby("session_id").timestamp.max() - results_df.groupby("session_id").timestamp.min())[-1]


def _get_average_time_per_session(results_df) -> float:
    return (results_df.groupby("session_id").timestamp.max() - results_df.groupby("session_id").timestamp.min()).mean()


def _is_super_user(end_date, start_date, results_df) -> bool:
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


def _get_data_from_mongo(end_date, start_date, user_id) -> Optional[pd.DataFrame]:
    _results_df = pd.DataFrame(
        list(MONGO_CLIENT.db.sessions.find({'client_user_id': user_id}))
    )
    return (
        _results_df[(_results_df.timestamp >= start_date) & (_results_df.timestamp <= end_date)]
        if len(_results_df) else None
    )
