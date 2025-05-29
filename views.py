def prompt_menu_choice():
    return input(">> ")

def prompt_date_time():
    return input("날짜 (YYMMDD),시간(HH:MM) >> ")

def prompt_id():
    return input("아이디 >> ")

def prompt_pw():
    return input("비밀번호 >> ")

def print_title():
    print("───────────────────────────────────────\n")
    print("           필라테스 예약 관리 시스템          \n")
    print("───────────────────────────────────────\n")

def print_date_time():
    print("───────────────────────────────────────\n")
    print("현재 날짜와 시간을 입력하세요.\n")
    print("날짜는 YYMMDD 형식, 시간은 24시간제 HH:MM형식입니다.\n")
    print("\n")
    print("예시: 240408,13:30\n")
    print("───────────────────────────────────────\n")

def print_main_menu():
    print("───────────────────────────────────────\n")
    print("1. 회원\n")
    print("2. 강사\n")
    print("3. 관리자\n")
    print("4. 종료\n")
    print("───────────────────────────────────────\n")

def print_register_login_menu():
    print("───────────────────────────────────────\n")
    print("1. 회원가입\n")
    print("2. 로그인\n")
    print("3. 시작 메뉴로 돌아가기\n")
    print("───────────────────────────────────────\n")

def print_login():
    print("───────────────────────────────────────\n")
    print("[로그인]\n")
    print("───────────────────────────────────────\n")

def print_error(message: str):
    """오류 메시지를 출력합니다."""
    print(f"[오류] {message}\n")

def print_user_id_rules():
    print("───────────────────────────────────────")
    print("[ 아이디 회원가입 규칙]")
    print(" - 5~16자, 영어/숫자/특수문자만 허용, 공백 불가, 영어로 시작해야 함")
    print(" - 예시 입력: user123!")
    print("───────────────────────────────────────")

def print_name_rules():
    print("───────────────────────────────────────")
    print("[ 이름 입력 규칙]")
    print(" - 길이 1이상, 공백류 불가, 한글/영어만 허용")
    print(" - 예시 입력: 조은영")
    print("───────────────────────────────────────")

def print_phone_rules():
    print("───────────────────────────────────────")
    print("[ 전화번호 입력 규칙]")
    print(" - 010으로 시작하는 11자리 숫자, 공백 불가")
    print(" - 예시 입력: 01041026022")
    print("───────────────────────────────────────")

def print_password_rules():
    print("───────────────────────────────────────")
    print("[ 비밀번호 입력 규칙]")
    print(" - 5~16자, 대문자로 시작, 특수문자+영어+숫자 포함, 반복문자 3회 이상 금지)")
    print(" - 예시 입력: A1bc3!")
    print("───────────────────────────────────────")

def print_signup_complete():
    print("회원가입이 완료되었습니다.\n")
