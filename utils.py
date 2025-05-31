import csv
import re
import os
from constants import SUCCESS, BASIC_ERROR, MEMBER_PATH, INSTRUCTOR_PATH, DATETIME_PATH, RESERVATION_PATH
from datetime import datetime, date
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
        # 파일이 비어있거나 데이터가 없는 경우 체크
        if not rows or not any(row and "datetime" in row for row in rows):
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

def has_minimum_reservations(user_id: str, start: date, end: date, min_count: int = 2) -> bool:
    try:
        with open(RESERVATION_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    class_date = datetime.strptime(row["날짜"], "%y%m%d").date()
                    if start <= class_date <= end:
                        student_ids = [s.strip() for s in row["수강 회원 id 리스트"].split(",")]
                        if user_id in student_ids:
                            count += 1
                    if count >= min_count:
                        return True
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return False