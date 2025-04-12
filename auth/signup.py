import csv
import os
from constants import MEMBER_PATH, INSTRUCTOR_PATH, INSTRUCTOR_CODE
from utils import validate_user_id, validate_name, validate_phone, validate_password, check_duplicate_id

def signup(user_type: str):
    is_instructor = user_type == '2'

    if is_instructor:
        while True:
            code = input("강사 인증코드를 입력하세요: ").strip()
            if code == INSTRUCTOR_CODE:
                break
            print("[오류] 올바른 인증 코드가 아닙니다.\n")

    # 아이디 입력 및 중복 확인
    while True:
        print("───────────────────────────────────────")
        print("[ 아이디 회원가입 규칙]")
        print(" - 5~16자, 영어/숫자/특수문자만 허용, 공백 불가, 영어로 시작해야 함")
        print(" - 예시 입력: user123!")
        print("───────────────────────────────────────")
        user_id = input("아이디를 입력하세요 >>").strip()
        if not validate_user_id(user_id):
            print("[오류] 아이디 규칙에 맞지 않습니다.\n")
            continue
        if check_duplicate_id(user_id, is_instructor):
            print("[오류] 동일한 아이디가 존재합니다.\n")
            continue
        break

    # 이름 입력
    while True:
        print("───────────────────────────────────────")
        print("[ 이름 입력 규칙]")
        print(" - 길이 1이상, 공백류 불가, 한글/영어만 허용")
        print(" - 예시 입력: 조은영")
        print("───────────────────────────────────────")
        name = input("이름을 입력하세요 >>").strip()
        if not validate_name(name):
            print("[오류] 이름 규칙에 맞지 않습니다.\n")
            continue
        break

    # 전화번호 입력
    while True:
        print("───────────────────────────────────────")
        print("[ 전화번호 입력 규칙]")
        print(" - 010으로 시작하는 11자리 숫자, 공백 불가")
        print(" - 예시 입력: 01041026022")
        print("───────────────────────────────────────")
        phone = input("전화번호를 입력하세요 >>").strip()
        if not validate_phone(phone):
            print("[오류] 전화번호 규칙에 맞지 않습니다.\n")
            continue
        break

    # 비밀번호 입력
    while True:
        print("───────────────────────────────────────")
        print("[ 비밀번호 입력 규칙]")
        print(" - 5~16자, 대문자로 시작, 특수문자+영어+숫자 포함, 반복문자 3회 이상 금지)")
        print(" - 예시 입력: A1bc3!")
        print("───────────────────────────────────────")
        password = input("비밀번호를 입력하세요 >>").strip()
        if not validate_password(password):
            print("[오류] 비밀번호 규칙에 맞지 않습니다.\n")
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

    print("회원가입이 완료되었습니다.\n")