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
        choice = input("숫자를 입력해주세요 >> ").strip()

        if not choice.isdigit() or choice not in ['1', '2', '3']:
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
    if len(my_classes) >= MAX_CLASSES_PER_INSTRUCTOR:
        print("[오류] 등록 가능한 수업 개수를 초과했습니다.\n")
        return

    while True:
        print("\n───────────────────────────────────────")
        print("[ 수업 등록 ]")
        print("───────────────────────────────────────")
        date_input = input("등록하고 싶은 날짜를 입력해주세요(YYMMDD) >> ").strip()
        if not re.match(r'^\d{6}$', date_input):
            print("[오류] 날짜 형식에 맞지 않습니다.\n")
            return

        try:
            date_obj = datetime.strptime(date_input, "%y%m%d")
            if date_obj.date() <= current_datetime.date():
                print("[오류] 이미 지난 날짜입니다.\n")
                return
        except ValueError:
            print("[오류] 날짜 형식에 맞지 않습니다.\n")
            return
        break

    time_table = [f"타임 {i:02d}: {8+i:02d}:00~{8+i:02d}:50" for i in range(15)]
    print("\n───────────────────────────────────────")
    print("[ 수업 등록 ]")
    for t in time_table:
        print(t)
    print("───────────────────────────────────────")
    
    time_input = input("등록하고 싶은 타임을 입력해주세요 >> ").strip()
    if not re.match(r'^[01][0-9]$', time_input):
        print("[오류] 타임 형식에 맞지 않습니다.\n")
        return
    if any(c for c in my_classes if c['날짜'] == date_input and c['타임'] == time_input):
        print("[오류] 이 타임에 이미 수업이 등록되어 있습니다.\n")
        return

    capacity = input("수업 정원을 입력해주세요 >> ").strip()
    if not capacity.isdigit() or not (1 <= int(capacity) <= 6):
        print("[오류] 1~6 숫자만 가능합니다.\n")
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
    input("아무 키나 누르면 메뉴 화면으로 돌아갑니다 >> ")