from controllers.locker_controller import LockerSystem

def show_instructor_menu(instructor: Instructor, current_datetime: datetime):
    locker_system = LockerSystem()
    while True:
        print("───────────────────────────────────────")
        print("1. 수업 등록")
        print("2. 수업 조회")
        print("3. 사물함 개수 설정")
        print("4. 로그아웃")
        print("───────────────────────────────────────")
        choice = input("숫자를 입력해주세요 >> ")

        # 공백 검사 추가 + 기존 오류 메시지로 통일
        if not re.fullmatch(r'[1-4]', choice):
            print("[오류] 1~4 숫자만 가능합니다\n")
            continue

        if choice == '1':
            register_class(instructor, current_datetime)
        elif choice == '2':
            view_classes(instructor)
        elif choice == '3':
            set_locker_count(locker_system)
        elif choice == '4':
            break

def set_locker_count(locker_system: LockerSystem):
    """사물함 개수를 설정합니다."""
    print("\n───────────────────────────────────────")
    print("[ 사물함 개수 설정 ]")
    print("───────────────────────────────────────")
    print(f"현재 사물함 개수: {len(locker_system.lockers)}")
    new_count = input("새로운 사물함 개수를 입력하세요 >> ")
    
    success, message = locker_system.set_locker_count(new_count)
    print(f"[{'완료' if success else '오류'}] {message}\n") 