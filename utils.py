import csv
import re
import os
from constants import SUCCESS, BASIC_ERROR, MEMBER_PATH, INSTRUCTOR_PATH, DATETIME_PATH
from datetime import datetime
from file_handler import read_csv, write_csv

def validate_datetime_input(user_input: str) -> int:
    if (user_input.count(',') != 1) or (' ' in user_input):
        return BASIC_ERROR

    date_str, time_str = user_input.split(',')

    if (len(date_str) != 6) or (len(time_str) != 5 or ':' not in time_str):
        return BASIC_ERROR

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

def validate_signup_id(user_id: str) -> bool:
    """회원가입 아이디 유효성 검사: 영문자와 숫자만 허용"""
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*]{4,15}$', user_id))

def validate_signup_name(name: str) -> bool:
    """회원가입 이름 유효성 검사"""
    return bool(re.match(r'^[가-힣a-zA-Z]+$', name))

def validate_signup_phone(phone: str) -> bool:
    """회원가입 전화번호 유효성 검사"""
    return bool(re.match(r'^010\d{8}$', phone))

def validate_signup_password(password: str) -> bool:
    """회원가입 비밀번호 유효성 검사"""
    # 기본 형식 확인: 대문자 시작, 허용 문자만, 길이 5~16자
    if not re.match(r'^[A-Z][A-Za-z0-9!@#$%^&*]{4,15}$', password):
        return False

    # 문자 조합 체크: 특수문자, 숫자, 영문 포함 여부
    has_letter = re.search(r'[a-zA-Z]', password)
    has_number = re.search(r'[0-9]', password)
    has_special = re.search(r'[!@#$%^&*]', password)

    if not (has_letter and has_number and has_special):
        return False

    # 반복 문자 3회 이상 금지
    if re.search(r'(.)\1\1', password):
        return False

    return True

def check_signup_duplicate_id(user_id: str, is_instructor: bool) -> bool:
    """회원가입 아이디 중복 검사"""
    path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return any(row['아이디'] == user_id for row in reader)
    return False
