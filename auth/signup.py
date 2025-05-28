from constants import MEMBER_PATH, INSTRUCTOR_PATH, INSTRUCTOR_CODE, USER_TYPE_INSTRUCTOR
from models import Instructor, Member
from file_handler import read_csv, write_csv
import views
import re

def get_instructor_code():
    while True:
        code = input("인증코드를 입력하세요 >>")

        # 공백 검사 + 코드 일치 검사
        if (code != code.strip()) or (code != INSTRUCTOR_CODE):
            views.print_error("올바른 인증 코드가 아닙니다.")
            continue
        break

def get_id(path: str) -> str:
    while True:
        views.print_user_id_rules()
        id = input("아이디를 입력하세요 >>")

        if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9!@#$%^&*]{4,15}', id):
            views.print_error("아이디 규칙에 맞지 않습니다.")
            continue
        if check_signup_duplicate_id(id, path):
            views.print_error("동일한 아이디가 존재합니다.")
            continue
        return id

def check_signup_duplicate_id(id: str, path: str) -> bool:
    """회원가입 아이디 중복 검사"""
    try:
        data = read_csv(path)
        return any(row['아이디'] == id for row in data)
    except FileNotFoundError:
        return False

def get_name() -> str:
    while True:
        views.print_name_rules()
        name = input("이름을 입력하세요 >>")
        if not re.fullmatch(r'[가-힣a-zA-Z]+', name):
            views.print_error("이름 규칙에 맞지 않습니다.")
            continue
        return name

def get_phone() -> str:
    while True:
        views.print_phone_rules()
        phone = input("전화번호를 입력하세요 >>")

        if not re.fullmatch(r'010\d{8}', phone):
            views.print_error("전화번호 규칙에 맞지 않습니다.")
            continue
        return phone

def get_password() -> str:
    while True:
        views.print_password_rules()
        password = input("비밀번호를 입력하세요 >>")
            
        # 같은 문자 3회 이상 연속 사용 불가
        if re.search(r'(.)\1\1', password):
            views.print_error("비밀번호 규칙에 맞지 않습니다.")
            continue
            
        # 비밀번호 정규식 검사 (통합 패턴)
        # 첫 글자가 이미 대문자이므로 영문자 검사는 소문자만 확인
        pattern = r'[A-Z](?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{4,15}'
        if not re.fullmatch(pattern, password):
            views.print_error("비밀번호 규칙에 맞지 않습니다.")
            continue
            
        return password

def save_user_to_csv(user_data: dict, path: str) -> None:
    """사용자 데이터를 CSV 파일에 저장합니다."""
    try:
        existing_data = read_csv(path)
    except FileNotFoundError:
        existing_data = []
    
    existing_data.append(user_data)
    write_csv(path, existing_data)

def signup(user_type: str) -> Member | Instructor:
    """사용자 회원가입 처리 함수"""
    is_instructor = (user_type == USER_TYPE_INSTRUCTOR)
    path = INSTRUCTOR_PATH if is_instructor else MEMBER_PATH

    # 강사 인증 코드 검사
    if is_instructor: get_instructor_code()

    id = get_id(path)
    name = get_name()
    phone = get_phone()
    password = get_password()

    user_data = {
        '아이디': id,
        '비밀번호': password,
        '이름': name,
        '전화번호': phone
    }

    # 회원 정보 저장
    save_user_to_csv(user_data, path)
    views.print_signup_complete()

    # 사용자 객체 반환
    if is_instructor:
        return Instructor(id=id, pw=password, name=name, ph=phone)
    return Member(id=id, pw=password, name=name, ph=phone)