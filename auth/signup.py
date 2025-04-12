import csv
import os
from constants import MEMBER_PATH, INSTRUCTOR_PATH, INSTRUCTOR_CODE, USER_TYPE_INSTRUCTOR
from utils import (
    validate_signup_id, validate_signup_name, validate_signup_phone,
    validate_signup_password, check_signup_duplicate_id
)
from models import Instructor, Member
import views

def verify_instructor_code():
    while True:
        code = input("인증코드를 입력하세요 >>").strip()
        if code == INSTRUCTOR_CODE:
            break
        views.print_error("올바른 인증 코드가 아닙니다.")

def get_user_id(is_instructor: bool) -> str:
    while True:
        views.print_user_id_rules()
        user_id = input("아이디를 입력하세요 >>").strip()
        if not validate_signup_id(user_id):
            views.print_error("아이디 규칙에 맞지 않습니다.")
            continue
        if check_signup_duplicate_id(user_id, is_instructor):
            views.print_error("동일한 아이디가 존재합니다.")
            continue
        return user_id

def get_name() -> str:
    while True:
        views.print_name_rules()
        name = input("이름을 입력하세요 >>").strip()
        if not validate_signup_name(name):
            views.print_error("이름 규칙에 맞지 않습니다.")
            continue
        return name

def get_phone() -> str:
    while True:
        views.print_phone_rules()
        phone = input("전화번호를 입력하세요 >>").strip()
        if not validate_signup_phone(phone):
            views.print_error("전화번호 규칙에 맞지 않습니다.")
            continue
        return phone

def get_password() -> str:
    while True:
        views.print_password_rules()
        password = input("비밀번호를 입력하세요 >>").strip()
        if not validate_signup_password(password):
            views.print_error("비밀번호 규칙에 맞지 않습니다.")
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

def signup(user_type: str) -> Member | Instructor:
    is_instructor = user_type == USER_TYPE_INSTRUCTOR

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

    if is_instructor:
        return Instructor(id=user_id, pw=password, name=name, phone=phone)
    return Member(id=user_id, pw=password, name=name, phone=phone)