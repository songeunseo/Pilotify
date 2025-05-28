from controllers.locker_controller import LockerSystem

class MemberSystem:
    def __init__(self, username, current_datetime: datetime):
        self.username = username
        self.current_datetime = current_datetime
        self.teachers_name = {instructor.id: instructor.name for instructor in load_instructor_data()}
        self.class_list = self.load_classes_from_csv()
        self.enrolled_classes = set()
        self.locker_system = LockerSystem()
    
    def show_menu(self):
        while True:
            print("───────────────────────────────────────────────")
            print("1. 수업 신청\n2. 수업 취소\n3. 신청 수업 조회\n4. 사물함 관리\n5. 로그아웃")
            print("───────────────────────────────────────────────")
            choice = input("숫자를 입력해주세요 >> ")

            # 공백 검사 + 숫자 검사 + 범위 검사
            if not re.fullmatch(r'[1-5]', choice):
                print("[오류] 1~5 숫자만 가능합니다")
                continue

            if choice == "1":
                self.apply_class()
            elif choice == "2":
                self.cancel_class()
            elif choice == "3":
                self.view_enrollments()
            elif choice == "4":
                self.manage_locker()
            elif choice == "5":
                print("로그아웃되었습니다.")
                break

    def manage_locker(self):
        """사물함 관리 메뉴를 표시합니다."""
        while True:
            print("───────────────────────────────────────────────")
            print("[ 사물함 관리 ]")
            print("1. 사물함 신청\n2. 사물함 반납\n3. 돌아가기")
            print("───────────────────────────────────────────────")
            choice = input("숫자를 입력해주세요 >> ")

            if not re.fullmatch(r'[1-3]', choice):
                print("[오류] 1~3 숫자만 가능합니다")
                continue

            if choice == "1":
                success, message = self.locker_system.assign_locker(self.username)
                print(f"[{'완료' if success else '오류'}] {message}")
            elif choice == "2":
                success, message = self.locker_system.release_locker(self.username)
                print(f"[{'완료' if success else '오류'}] {message}")
            elif choice == "3":
                break 