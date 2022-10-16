from sys import exit
from user import CurrentUser


def get_top_5_users():
    print('Top 5 users')


def get_7_days_status():
    print('7 days status')


def predict_session_duration():
    print('5')


def save_to_txt():
    print('Saved to txt')


def exit_program():
    exit()


def print_summary():
    print(f'User id: {CurrentUser().user_id}, period: {CurrentUser().period}')


def enter_user_id():
    CurrentUser().user_id = input()


def enter_period():
    CurrentUser().period = input()
