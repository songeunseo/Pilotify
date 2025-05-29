import re
from utils import read_csv, write_csv
from constants import *
from datetime import datetime
from controllers.locker_controller import LockerSystem

def show_admin_menu(current_datetime: datetime):
    locker_system = LockerSystem()
    while True:
        print("───────────────────────────────────────")
        print("[ 관리자 메뉴 ]")
        print("───────────────────────────────────────")
        print("1. 수업 취소 승인 (구현 예정)")
        print("2. 사물함 강제 퇴거")
        print("3. 사물함 개수 설정")
        print("4. 강사 인증 코드 수정")
        print("5. 로그아웃")
        print("───────────────────────────────────────")
        choice = input("숫자를 입력해주세요 >> ")

        # 공백 검사 추가 + 기존 오류 메시지로 통일
        if not re.fullmatch(r'[1-5]', choice):
            print("[오류] 1~5 숫자만 가능합니다\n")
            continue

        if choice == '1':
            print("[안내] 수업 취소 승인 기능은 구현 예정입니다.\n")
            pass # TODO: 수업 취소 승인 기능 구현
        elif choice == '2':
            locker_forced_eviction(locker_system, current_datetime)
        elif choice == '3':
            set_locker_count(locker_system)
        elif choice == '4':
            set_instructor_code(current_datetime)
        elif choice == '5':
            break

def locker_forced_eviction(locker_system: LockerSystem, current_datetime:datetime)-> None:
    """사물함을 강제퇴거합니다."""
    print("\n───────────────────────────────────────")
    print("[ 사물함 강제 퇴거 ] \n")
    locker_system.print_locker_status(current_datetime = current_datetime)
    user_input = input("강제 퇴거할 사물함 번호를 입력해주세요 >>")

    if not re.fullmatch(r"^\d{2}$", user_input):
        print("[오류] 입력 형식에 맞지 않습니다.")
        return
    elif not locker_system.is_occupied(user_input):
        print("[오류] 이용 중인 사물함이 아닙니다.")
        return
    else:
        locker_system.release_locker_forced(id = id)
        print("강제 퇴거 완료되었습니다.") 
    return  

def set_locker_count(locker_system: LockerSystem):
    """사물함 개수를 설정합니다."""
    print("\n───────────────────────────────────────")
    print("[ 사물함 개수 설정 ]")
    print("───────────────────────────────────────")
    print(f"현재 사물함 개수: {len(locker_system.lockers)}")
    new_count = input("새로운 사물함 개수를 입력하세요 >> ")
    
    success, message = locker_system.set_locker_count(new_count)
    print(f"[{'완료' if success else '오류'}] {message}\n")

def set_instructor_code(current_datetime:datetime)->None:
    rows = read_csv(INST_CODE_PATH)
    if not rows:
        last_modified_date = f"{current_datetime:%y%m%d}"
        current_code = "0000"
        write_csv(INST_CODE_PATH, [{"last_modified_date": last_modified_date, "current_code": current_code}])
    else:
        last_modified_date = rows[0]["last_modified_date"]
        current_code = rows[0]["current_code"]

    print("───────────────────────────────────────")
    print("[ 강사 인증 코드 설정 ]")
    print("───────────────────────────────────────")
    print(f"현재 인증 코드: {current_code}")
    new_code = input("새로운 인증 코드를 입력하세요 (4자리 숫자) >> ")

    if not re.fullmatch(r"^\d{4}$", new_code):
        print("[오류] 올바른 인증코드가 아닙니다.")
        return
    if new_code == current_code:
        print("[오류] 현재 인증 코드와 동일한 값으로는 변경할 수 없습니다.")
        return
    if f"{current_datetime:%y%m}" == last_modified_date[:4]:
        next_month = current_datetime.month + 1
        next_year = current_datetime.year
        if next_month > 12: next_month = 1; next_year += 1
        print(f"[오류] 이번 달에는 이미 인증 코드를 변경했습니다. 다음 변경 가능 시점: {next_year}년 {next_month}월 1일부터")
        return

    write_csv(INST_CODE_PATH, [{"last_modified_date": f"{current_datetime:%y%m%d}", "current_code": new_code}])
    print("인증 코드가 정상적으로 변경되었습니다.")
    return