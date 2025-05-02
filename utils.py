import csv
import re
import os
from constants import SUCCESS, BASIC_ERROR, MEMBER_PATH, INSTRUCTOR_PATH, DATETIME_PATH
from datetime import datetime
from file_handler import read_csv, write_csv

def validate_datetime_input(user_input: str) -> int:
    # 정규식으로 날짜,시간 형식 검사 (YYMMDD,HH:MM 형식)
    if not re.fullmatch(r'\d{6},\d{2}:\d{2}', user_input):
        return BASIC_ERROR

    date_str, time_str = user_input.split(',')
    
    try:
        # 입력된 날짜 해석
        input_year = int(date_str[:2])
        input_month = int(date_str[2:4])
        input_day = int(date_str[4:6])

        if 0 <= input_year <= 68:
            input_full_year = 2000 + input_year
        else:
            input_full_year = 2000 + input_year

        input_hour = int(time_str[:2])
        input_minute = int(time_str[3:5])

        input_datetime = datetime(input_full_year, input_month, input_day, input_hour, input_minute)

        rows = read_csv(DATETIME_PATH)
        if rows and rows[0]:
            last_date = rows[0]["datetime"] if isinstance(rows[0], dict) else rows[0][0]
            last_date_str, last_time_str = last_date.split(',')

            # 저장된 날짜 해석
            last_year = int(last_date_str[:2])
            last_month = int(last_date_str[2:4])
            last_day = int(last_date_str[4:6])

            if 0 <= last_year <= 68:
                last_full_year = 2000 + last_year
            else:
                last_full_year = 2000 + last_year

            last_hour = int(last_time_str[:2])
            last_minute = int(last_time_str[3:5])

            last_datetime = datetime(last_full_year, last_month, last_day, last_hour, last_minute)

            if input_datetime >= last_datetime:
                write_csv(DATETIME_PATH, [{"datetime": user_input}])
                return SUCCESS
            else:
                return BASIC_ERROR
        else:
            # 파일 비어있으면 그냥 기록
            write_csv(DATETIME_PATH, [{"datetime": user_input}])
            return SUCCESS

    except (ValueError, IndexError, KeyError):
        return BASIC_ERROR

def validate_menu_choice(user_input: str, valid_choices: list[str]) -> bool:
    # 입력이 숫자이고, 선택지 안에 있는지 검사
    if user_input.isdigit() and user_input in valid_choices:
        return SUCCESS
    return BASIC_ERROR

def validate_login_id(id: str, user_list: list):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', id):
        return BASIC_ERROR, None
    for user in user_list:
        if user.id == id:
            return SUCCESS, user
        #확인
    
    return BASIC_ERROR, None
