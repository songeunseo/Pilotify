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
        # 입력 날짜,시간 파싱
        input_year = int(date_str[:2]) + 2000
        input_month = int(date_str[2:4])
        input_day = int(date_str[4:6])
        input_hour, input_minute = map(int, time_str.split(':'))
        input_datetime = datetime(input_year, input_month, input_day, input_hour, input_minute)

        rows = read_csv(DATETIME_PATH)
        # 파일 비어있으면(헤더만 존재) 그냥 기록
        if len(rows) == 1:
            write_csv(DATETIME_PATH, [{"datetime": user_input}])
            return SUCCESS

        last_date_str, last_time_str = rows[0]["datetime"].split(',')
        last_year = int(last_date_str[:2]) + 2000
        last_month = int(last_date_str[2:4])
        last_day = int(last_date_str[4:6])
        last_hour, last_minute = map(int, last_time_str.split(':'))
        last_datetime = datetime(last_year, last_month, last_day, last_hour, last_minute)

        # 입력된 날짜가 마지막 저장 날짜보다 이후인지 확인
        if input_datetime >= last_datetime:
            write_csv(DATETIME_PATH, [{"datetime": user_input}])
            return SUCCESS
        else:
            return BASIC_ERROR
                
    except (ValueError, IndexError, KeyError):
        return BASIC_ERROR

def validate_login_id(id: str, user_list: list):
    if not re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', id):
        return BASIC_ERROR, None
    for user in user_list:
        if user.id == id:
            return SUCCESS, user
    
    return BASIC_ERROR, None
