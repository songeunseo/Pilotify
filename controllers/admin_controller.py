import re
from utils import read_csv, write_csv
from constants import *
from datetime import datetime, time
from controllers.locker_controller import LockerSystem

# 타임 정보 정의
TIME_SLOTS = {
    "00": (time(8, 0), time(8, 50)),
    "01": (time(9, 0), time(9, 50)),
    "02": (time(10, 0), time(10, 50)),
    "03": (time(11, 0), time(11, 50)),
    "04": (time(12, 0), time(12, 50)),
    "05": (time(13, 0), time(13, 50)),
    "06": (time(14, 0), time(14, 50)),
    "07": (time(15, 0), time(15, 50)),
    "08": (time(16, 0), time(16, 50)),
    "09": (time(17, 0), time(17, 50)),
    "10": (time(18, 0), time(18, 50)),
    "11": (time(19, 0), time(19, 50)),
    "12": (time(20, 0), time(20, 50)),
    "13": (time(21, 0), time(21, 50)),
    "14": (time(22, 0), time(22, 50))
}

def show_admin_menu(current_datetime: datetime):
    locker_system = LockerSystem()
    while True:
        print("───────────────────────────────────────")
        print("[ 관리자 메뉴 ]")
        print("───────────────────────────────────────")
        print("1. 수업 취소 승인")
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
            accept_cancellation(current_datetime)
        elif choice == '2':
            locker_forced_eviction(locker_system, current_datetime)
        elif choice == '3':
            set_locker_count(locker_system)
        elif choice == '4':
            set_instructor_code(current_datetime)
        elif choice == '5':
            locker_system.save_lockers()
            break

def accept_cancellation(current_datetime: datetime) -> int:
    cancellations = read_csv(CANCELLATION_PATH)
    reservations = read_csv(RESERVATION_PATH)

    # 1. 현재 날짜와 시간 이전 수업에 대한 취소 요청 자동 삭제
    valid_cancellations = []
    for ca in cancellations:
        class_id = ca['class_id']
        # 해당 class_id의 수업 정보 찾기
        reservation = next((r for r in reservations if r['아이디'].strip() == class_id), None)
        if reservation:
            class_date = reservation['날짜'].strip()
            class_time = reservation['타임'].strip()
            # 날짜와 시간 비교
            class_dt = datetime.strptime(class_date, "%y%m%d")
            if class_time in TIME_SLOTS:
                start_time = TIME_SLOTS[class_time][0]
                class_dt = datetime.combine(class_dt.date(), start_time)
                if class_dt > current_datetime:
                    valid_cancellations.append(ca)
    cancellations = valid_cancellations
    write_csv(CANCELLATION_PATH, cancellations)

    # 2. 취소 신청 데이터 리스트 출력
    print("───────────────────────────────────────────────")
    print("[ 수업 취소 승인 ]")
    print("───────────────────────────────────────────────")
    print("취소 신청 ID | 수업 ID | 회원 이름 |")
    print("───────────────────────────────────────────────")
    for ca in cancellations:
        print(f"        {ca['cancellation_id']:<8}{ca['class_id']:<9}{ca['user_name']:<9}")
    print("───────────────────────────────────────────────")

    # 3. 승인할 수업 취소 ID 입력
    ca_id = input("승인할 취소 신청 ID를 입력하세요 >> ")

    # 3-1. 취소 신청 유효성 검증
    if not cancellations:
        print("[오류] 현재 취소 신청된 수업이 없습니다.")
        return -1

    # 3-2. ca_id값 검증
    if not re.fullmatch(r'^\d+$', ca_id):
        print("[오류] 입력 형식에 맞지 않습니다.")
        return -2

    # 3-3. 취소 신청 데이터에서 해당 항목 찾기
    for cancellation in cancellations:
        if cancellation['cancellation_id'] == ca_id:
            ca_class_id = cancellation['class_id']
            ca_member_id = cancellation['user_id']
            # 해당 항목 제거
            cancellations = [c for c in cancellations if c['cancellation_id'] != ca_id]
            break
    else:
        print("[오류] 유효하지 않은 취소 신청 ID 입니다.")
        return -3

    # 4. 수업 데이터에서 해당 회원 제거
    for reservation in reservations:
        if reservation['아이디'].strip() == ca_class_id:
            raw_users = reservation['수강 회원 id 리스트'].strip().strip('"')
            user_ids = [uid.strip() for uid in raw_users.split(",")] if raw_users else []
            if ca_member_id in user_ids:
                user_ids.remove(ca_member_id)
                reservation['수강 회원 id 리스트'] = ",".join(user_ids)

    # 5. 파일 저장
    write_csv(CANCELLATION_PATH, cancellations)
    write_csv(RESERVATION_PATH, reservations)

    print("취소 승인 완료되었습니다.")
    return 0

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
        locker_system.release_locker_forced(user_input)
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
    try:
        rows = read_csv(INST_CODE_PATH)
    except FileNotFoundError:
        print("[오류] 인증 코드 파일이 존재하지 않습니다.")
        return
    
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