import csv
import os
from constants import MEMBER_PATH, INSTRUCTOR_PATH, INSTRUCTOR_CODE
from utils import (
    validate_signup_id, validate_signup_name, validate_signup_phone,
    validate_signup_password, check_signup_duplicate_id
)
import views

def verify_instructor_code():
    while True:
        views.print_instructor_code_prompt()
        code = input().strip()
        if code == INSTRUCTOR_CODE:
            break
        views.print_error_invalid_code()

def get_user_id(is_instructor: bool) -> str:
    while True:
        views.print_user_id_rules()
        user_id = input("아이디를 입력하세요 >>").strip()
        if not validate_signup_id(user_id):
            views.print_error_invalid_id()
            continue
        if check_signup_duplicate_id(user_id, is_instructor):
            views.print_error_duplicate_id()
            continue
        return user_id

def get_name() -> str:
    while True:
        views.print_name_rules()
        name = input("이름을 입력하세요 >>").strip()
        if not validate_signup_name(name):
            views.print_error_invalid_name()
            continue
        return name

def get_phone() -> str:
    while True:
        views.print_phone_rules()
        phone = input("전화번호를 입력하세요 >>").strip()
        if not validate_signup_phone(phone):
            views.print_error_invalid_phone()
            continue
        return phone

def get_password() -> str:
    while True:
        views.print_password_rules()
        password = input("비밀번호를 입력하세요 >>").strip()
        if not validate_signup_password(password):
            views.print_error_invalid_password()
            continue
        return password

def save_user_data(user_data: dict, is_instructor: bool):
    fieldnames = ['아이디', '비밀번호', '이름', '전화번호']
    path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH
    
    file_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(user_data)

def signup(user_type: str):
    is_instructor = user_type == '2'

    if is_instructor:
        verify_instructor_code()

    user_id = get_user_id(is_instructor)
    name = get_name()
    phone = get_phone()
    password = get_password()

    user_data = {
        '아이디': user_id,
        '비밀번호': password,
        '이름': name,
        '전화번호': phone
    }

    save_user_data(user_data, is_instructor)
    views.print_signup_complete()