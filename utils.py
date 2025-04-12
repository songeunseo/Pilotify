import csv
import re
import os
from constants import SUCCESS, BASIC_ERROR, GRAMMAR_ERROR, NO_DUPLICATION
from constants import USER_TYPE_INSTRUCTOR, USER_TYPE_MEMBER, MEMBER_PATH, INSTRUCTOR_PATH
from datetime import datetime
from models import Member, Instructor

def validate_datetime_input(user_input: str) -> int:
    # 콤마가 정확히 한 개여야 함, 공백이 없어야 함
    if (user_input.count(',') != 1) or (' ' in user_input):
        return BASIC_ERROR

    date_str, time_str = user_input.split(',')

    # 날짜는 6자리, 시간은 5자리 + ':' 포함
    if (len(date_str) != 6) or (len(time_str) != 5 or ':' not in time_str):
        return BASIC_ERROR

    # 실제 존재하는 날짜/시간인지 확인
    try:
        datetime.strptime(date_str + ' ' + time_str, "%y%m%d %H:%M")
    except ValueError:
        return BASIC_ERROR

    return SUCCESS

def validate_menu_choice(user_input: str, valid_choices: list[str]) -> bool:
    # 입력이 숫자이고, 선택지 안에 있는지 검사
    if user_input.isdigit() and user_input in valid_choices:
        return SUCCESS
    return BASIC_ERROR

def validate_id(id: str, user_list: list):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', id):
        return BASIC_ERROR, None
    for user in user_list:
        if user.id == id:
            return SUCCESS, user
    
    return BASIC_ERROR, None

def validate_user_id(user_id: str) -> bool:
    """아이디 유효성 검사"""
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', user_id))

def validate_name(name: str) -> bool:
    """이름 유효성 검사"""
    return bool(re.match(r'^[가-힣a-zA-Z]+$', name))

def validate_phone(phone: str) -> bool:
    """전화번호 유효성 검사"""
    return bool(re.match(r'^010\d{8}$', phone))

def validate_password(password: str) -> bool:
    """비밀번호 유효성 검사"""
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

def check_duplicate_id(user_id: str, is_instructor: bool) -> bool:
    """아이디 중복 검사"""
    path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return any(row['아이디'] == user_id for row in reader)
    return False