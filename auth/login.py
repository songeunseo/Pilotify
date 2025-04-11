import csv
import re

SUCCESS = 0
BASIC_ERROR = -1
GRAMMAR_ERROR = -2
NO_DUPLICATION = -3

MEMBER_PATH = 'data/members.csv'
INSTRUCTOR_PATH = 'data/instructor.csv'
CLASS_PATH = 'data/members.csv'

#회원 정보 클래스 생성
class Member_Data:
    id : str
    pw : str
    name : str
    ph : str
    tnum : int

class Instructor_Data:
    id : str
    pw : str
    name : str
    ph : str

#회원 정보 객체 배열 선언
member_data = []
instructor_data = []

#회원 정보 객체 배열 생성
def create_member_data():
    with open (MEMBER_PATH, newline=' ', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            member_data[reader] = Member_Data(row['id'], row['pw'], row['name'], row['ph'], row['tnum'])

    return member_data

#강사 정보 객체 배열 생성
def create_instructor_data():
    with open (INSTRUCTOR_PATH, newline=' ', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            instructor_data[reader] = Instructor_Data(row['id'], row['pw'], row['name'], row['ph'])

    return instructor_data

def is_valid_password(pw: str):
    # 기본 형식 확인: 대문자 시작, 허용 문자만, 길이 5~16자
    if not re.match(r'^[A-Z][A-Za-z0-9!@#$%^&*]{4,15}$', pw):
        return BASIC_ERROR

    # 문자 조합 체크: 특수문자, 숫자, 영문 포함 여부
    has_letter = re.search(r'[a-zA-Z]', pw)
    has_number = re.search(r'[0-9]', pw)
    has_special = re.search(r'[!@#$%^&*]', pw)

    if not (has_letter and has_number and has_special):
        return GRAMMAR_ERROR

    # 반복 문자 3회 이상 금지
    if re.search(r'(.)\1\1', pw):  # 같은 문자가 3번 연속
        return NO_DUPLICATION

    return SUCCESS

def login_id():
    while True:
        id = input()
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-]{4,15}$', id):
            print("[오류] 아이디 규칙에 맞지 않습니다.\n")

        else:
            for i in range(len(member_data)):
                if member_data[i](id) == id:
                    return member_data[i]

def login_pw(i: int):
    while True:
        pw = input()
        if is_valid_password(pw) == 0:
            if member_data[i](pw) == pw:
                return member_data[i]
        elif is_valid_password(pw) == -1:
            print("")

        elif is_valid_password(pw) == -2:
            print("")

        elif is_valid_password(pw) == -3:
            print("")