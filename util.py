from datetime import datetime, timedelta
from pytz import timezone
import time

import config
import date_type
import requests
import shutil
import os

dir_project = os.path.dirname(os.path.realpath(__file__))


def format_date(date: datetime, type_date: date_type.DateType) -> str:
    # Convert to type datetime
    # formatted_datetime = datetime.strptime(
    #       datenow_formatted, str(date_type.Fdate))

    if type_date == date_type.Date:
        datenow_formatted = datetime.strftime(date, date_type.Fdate)
        return datenow_formatted

    if type_date == date_type.Datetime1:
        datenow_formatted = datetime.strftime(date, date_type.Fdatetime1)
        return datenow_formatted

    datenow_formatted = datetime.strftime(date, date_type.Fdatetime2)
    return datenow_formatted


def timesmap_to_date(timestamp: float, time_zone: str):
    """Returns timestamp  timezone

    :param timestamp: float
    :param time_zone: string

    :return: datetime.datetime
    """
    timestamp = float(timestamp)

    date = datetime.fromtimestamp(timestamp, tz=timezone(time_zone))

    return date


def date_to_timestamp(date: str) -> int:
    """ Convert date to timestamp
    - Example:
        * date_to_timestamp('2023-04-10 00:00:00')
        * 1681095600

    :param date: str
        - Date complete format %Y-%m-%d %H:%M:%S

    :return: int
    """

    timestamp = int(time.mktime(
            time.strptime(
                str(date),
                date_type.Fdatetime2
            )
        )
    )
    return timestamp


def datetime_now_sum_days(date: datetime, days: int):
    sum_day = date + timedelta(days=days)
    return sum_day


def download_image(url, path, file_name):
    res = requests.get(url, stream=True)

    download_path = f'{path}\\{file_name}'

    if res.status_code == 200:
        with open(download_path, 'wb') as f:
            shutil.copyfileobj(res.raw, f)

        path_image = f'{path}\\{file_name}'

        return True, path_image
    else:
        default_path = f'{dir_project}\\img\\streaming-logo\\astronauta.png'
        return False, default_path


def get_datetime_sao_paulo():
    api_timezone = config.TIME_ZONE
    url_api = config.URL_API_DATETIME

    url_formatted = url_api.format(timezone=api_timezone)

    res = requests.get(url_formatted)

    if not res.status_code == 200:
        return datetime.now()

    response_date = res.json()['date']
    response_time = res.json()['time']
    response_sec = res.json()['seconds']

    union = f'{response_date} {response_time}:{str(response_sec)}'

    response_now = datetime.strptime(union, "%m/%d/%Y %H:%M:%S")

    return response_now
