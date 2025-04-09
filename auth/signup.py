import csv
import os
import re

MEMBER_PATH = 'data/members.csv'
INSTRUCTOR_PATH = 'data/instructor.csv'
INSTRUCTOR_CODE = '0000'  # 강사 인증코드

def is_valid_password(pw: str) -> bool:
    # 기본 형식 확인: 대문자 시작, 허용 문자만, 길이 5~16자
    if not re.match(r'^[A-Z][A-Za-z0-9!@#$%^&*]{4,15}$', pw):
        return False

    # 문자 조합 체크: 특수문자, 숫자, 영문 포함 여부
    has_letter = re.search(r'[a-zA-Z]', pw)
    has_number = re.search(r'[0-9]', pw)
    has_special = re.search(r'[!@#$%^&*]', pw)

    if not (has_letter and has_number and has_special):
        return False

    # 반복 문자 3회 이상 금지
    if re.search(r'(.)\1\1', pw):  # 같은 문자가 3번 연속
        return False

    return True

def signup(user_type: str):
    is_instructor = user_type == '2'

    if is_instructor:
        while True:
            code = input("강사 인증코드를 입력하세요: ").strip()
            if code == INSTRUCTOR_CODE:
                break
            print("[오류] 올바른 인증 코드가 아닙니다.")

    # 아이디 입력 및 중복 확인
    while True:
        print("───────────────────────────────────────")
        print("[ 아이디 회원가입 규칙]")
        print(" - 5~16자, 영어/숫자/특수문자만 허용, 공백 불가, 영어로 시작해야 함")
        print(" - 예시 입력: user123!")
        print("───────────────────────────────────────")
        user_id = input("아이디를 입력하세요 >>").strip()
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', user_id):
            print("[오류] 아이디 규칙에 맞지 않습니다.")
            continue

        path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if any(row['아이디'] == user_id for row in reader):
                    print("[오류] 동일한 아이디가 존재합니다.")
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
        if not re.match(r'^[가-힣a-zA-Z]+$', name):
            print("[오류] 이름 규칙에 맞지 않습니다.")
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
        if not re.match(r'^010\d{8}$', phone):
            print("[오류] 전화번호 규칙에 맞지 않습니다.")
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
        if not is_valid_password(password):
            print("[오류] 비밀번호 규칙에 맞지 않습니다.")
            continue
        break

    # CSV 저장
    fieldnames = ['아이디', '비밀번호', '이름', '전화번호']
    if not is_instructor:
        fieldnames.append('수강권')

    data = {
        '아이디': user_id,
        '비밀번호': password,
        '이름': name,
        '전화번호': phone
    }

    if not is_instructor:
        data['수강권'] = 5  # 회원가입 시 기본 수강권

    file_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    print("회원가입이 완료되었습니다.")