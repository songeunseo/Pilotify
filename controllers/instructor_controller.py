import csv
from datetime import datetime
from file_handler import read_csv, write_csv
from utils import *
from constants import *
from models import Instructor

def show_instructor_menu(instructor: Instructor, current_datetime: datetime):
    while True:
        print("───────────────────────────────────────")
        print("1. 수업 등록")
        print("2. 수업 조회")
        print("3. 로그아웃")
        print("───────────────────────────────────────")
        choice = input("숫자를 입력해주세요 >> ")

        # 공백 검사 추가 + 기존 오류 메시지로 통일
        if (choice != choice.strip()) or (not choice.isdigit()) or (choice not in ['1', '2', '3']):
            print("[오류] 1~3 숫자만 가능합니다\n")
            continue

        if choice == '1':
            register_class(instructor, current_datetime)
        elif choice == '2':
            view_classes(instructor)
        elif choice == '3':
            break

def register_class(instructor: Instructor, current_datetime: datetime):
    classes = read_csv(CLASS_PATH)
    my_classes = [c for c in classes if c['강사 id'] == instructor.id]
    if classes and int(classes[-1]['아이디']) >= 9999:
        print("[오류] 등록 가능한 수업 개수가 4자리를 초과하였습니다.\n")
        return

    print("\n───────────────────────────────────────")
    print("[ 수업 등록 ]")
    print("───────────────────────────────────────")
    date_input = input("등록하고 싶은 날짜를 입력해주세요(YYMMDD) >> ")
    
    # 공백 검사 + 날짜 형식 검사
    if (date_input != date_input.strip()) or (not re.match(r'^\d{6}$', date_input)):
        print("[오류] 날짜 형식에 맞지 않습니다.\n")
        return
    
    try:
        year = int(date_input[:2])
        month_day = date_input[2:]

        if not (0 <= year <= 99) or len(month_day) != 4:
            raise ValueError

    # 년도 직접 해석하기
        if 0 <= year <= 68:
            full_year = 2000 + year
        else:
            full_year = 2100 + (year - 100) if year < 69 else 2000 + year  # 69~99는 2069~2099로

    # 날짜 객체 만들기
        date_obj = datetime.strptime(f"{full_year}{month_day}", "%Y%m%d")

        if date_obj.date() < current_datetime.date():
            print("[오류] 이미 지난 날짜입니다.\n")
            return

    except ValueError:
        print("[오류] 날짜 형식에 맞지 않습니다.\n")
        return
    # try:
    #     date_obj = datetime.strptime(date_input, "%y%m%d")
    #     if date_obj.date() < current_datetime.date():
    #         print("[오류] 이미 지난 날짜입니다.\n")
    #         return
    # except ValueError:
    #     print("[오류] 날짜 형식에 맞지 않습니다.\n")
    #     return

    time_table = [f"타임 {i:02d}: {8+i:02d}:00~{8+i:02d}:50" for i in range(15)]
    print("\n───────────────────────────────────────")
    print("[ 수업 등록 ]")
    for t in time_table:
        print(t)
    print("───────────────────────────────────────")
    
    time_input = input("등록하고 싶은 타임을 입력해주세요 >> ")

    # 공백 검사 + 타임 형식 검사
    if (time_input != time_input.strip()) or (not re.match(r'^[01][0-4]$', time_input)):
        print("[오류] 타임 형식에 맞지 않습니다.\n")
        return
    
    # 1단계: 오늘 날짜인 경우 시간 비교
    if date_input == current_datetime.strftime("%y%m%d"):
    # 타임을 실제 시간으로 변환
        time_hour = int(time_input) + 8  # 타임 00 = 8시, 타임 01 = 9시, ...

    # 현재 시간 꺼내기
        now_hour = current_datetime.hour
        now_minute = current_datetime.minute

    # 만약 현재 시간이 타임 시작 시각을 넘었으면 오류
        if now_hour > time_hour or (now_hour == time_hour and now_minute > 0):
            print("[오류] 이미 지난 시간입니다.\n")
            return

    if any(c for c in my_classes if c['날짜'] == date_input and c['타임'] == time_input):
        print("[오류] 이 타임에 이미 수업이 등록되어 있습니다.\n")
        return

    capacity = input("수업 정원을 입력해주세요 >> ")

# 공백 검사 + 숫자 검사 + 1~6 범위 + 앞자리 0 금지
    if (capacity != capacity.strip()) or (not capacity.isdigit()) or (capacity.startswith('0')) or not (1 <= int(capacity) <= 6):
        print("[오류] 1~6 숫자만 가능합니다.\n")
        return

# 같은 날짜, 같은 타임에 있는 모든 수업의 정원 합을 계산
    current_total_capacity = sum(int(c['정원']) for c in classes if c['날짜'] == date_input and c['타임'] == time_input)

    if current_total_capacity + int(capacity) > 20:
        print(f"[오류] 해당 날짜와 타임에 등록된 총 정원이 {current_total_capacity}/20 입니다. 추가 등록이 불가합니다.\n")
        return
    
    new_id = f"{int(classes[-1]['아이디']) + 1:04d}" if classes else "0001"
    new_class = {
        "아이디": new_id,
        "날짜": date_input,
        "강사 id": instructor.id,
        "타임": time_input,
        "정원": capacity,
        "수강 회원 id 리스트": ""
    }
    classes.append(new_class)
    write_csv(CLASS_PATH, classes)
    print("수업 등록 완료되었습니다.\n")

def view_classes(instructor: Instructor):
    classes = read_csv(CLASS_PATH)
    my_classes = [c for c in classes if c['강사 id'] == instructor.id]
    
    if not my_classes:
        print("[오류] 등록된 수업이 없습니다.\n")
        return
    
    # 날짜순으로 정렬
    my_classes.sort(key=lambda x: x['날짜'])
    
    print("\n───────────────────────────────────────")
    print("  수업 ID  |    날짜    |   이름   |     타임      |  정원  |  신청 인원  |")
    print("───────────────────────────────────────")
    for c in my_classes:
        time = f"{int(c['타임'])+8:02d}:00-{int(c['타임'])+8:02d}:50"  # 타임을 실제 시간으로 변환
        print(f"   {c['아이디']:>4}     {c['날짜']}     {instructor.name}     {time}       {c['정원']:>2}             {len(c['수강 회원 id 리스트'].split(',')) if c['수강 회원 id 리스트'] else 0}")
    print("───────────────────────────────────────")
    input("엔터키를 누르면 메뉴 화면으로 돌아갑니다 >> ")