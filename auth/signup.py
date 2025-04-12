import csv
import os
from constants import MEMBER_PATH, INSTRUCTOR_PATH, INSTRUCTOR_CODE
from utils import validate_user_id, validate_name, validate_phone, validate_password, check_duplicate_id
import views

def signup(user_type: str):
    is_instructor = user_type == '2'

    if is_instructor:
        while True:
            views.print_instructor_code_prompt()
            code = input().strip()
            if code == INSTRUCTOR_CODE:
                break
            views.print_error_invalid_code()

    # 아이디 입력 및 중복 확인
    while True:
        views.print_user_id_rules()
        user_id = input("아이디를 입력하세요 >>").strip()
        if not validate_user_id(user_id):
            views.print_error_invalid_id()
            continue
        if check_duplicate_id(user_id, is_instructor):
            views.print_error_duplicate_id()
            continue
        break

    # 이름 입력
    while True:
        views.print_name_rules()
        name = input("이름을 입력하세요 >>").strip()
        if not validate_name(name):
            views.print_error_invalid_name()
            continue
        break

    # 전화번호 입력
    while True:
        views.print_phone_rules()
        phone = input("전화번호를 입력하세요 >>").strip()
        if not validate_phone(phone):
            views.print_error_invalid_phone()
            continue
        break

    # 비밀번호 입력
    while True:
        views.print_password_rules()
        password = input("비밀번호를 입력하세요 >>").strip()
        if not validate_password(password):
            views.print_error_invalid_password()
            continue
        break

    # CSV 저장
    fieldnames = ['아이디', '비밀번호', '이름', '전화번호']

    data = {
        '아이디': user_id,
        '비밀번호': password,
        '이름': name,
        '전화번호': phone
    }

    path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH
    file_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    views.print_signup_complete()