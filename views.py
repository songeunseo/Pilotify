def prompt_menu_choice():
    return input(">> ")

def prompt_date_time():
    return input("날짜 (YYMMDD),시간(HH:MM) >> ")

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
    print("3. 종료\n")
    print("───────────────────────────────────────\n")

def print_register_login_menu():
    print("───────────────────────────────────────\n")
    print("1. 회원가입\n")
    print("2. 로그인\n")
    print("3. 시작 메뉴로 돌아가기\n")
    print("───────────────────────────────────────\n")