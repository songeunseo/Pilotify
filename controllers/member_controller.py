import csv
from file_handler import *
from controllers.locker_controller import LockerSystem
from datetime import datetime, timedelta
from constants import *
import re

class ClassSession:
    def __init__(self, session_id, date, time, teacher_id, enrolled_user_ids, capacity,instructor_names):
        self.session_id = session_id
        self.date = date 
        self.time = int(time)
        self.teacher_id = teacher_id
        self.enrolled_user_ids = enrolled_user_ids
        self.capacity = int(capacity)
        self.instructor_name = instructor_names.get(teacher_id, "Unknown")

    def is_full(self):
        return len(self.enrolled_user_ids) >= self.capacity

    def is_past(self, current_datetime: datetime):
        class_date = datetime.strptime(self.date, "%y%m%d")
        class_time = int(self.time) + 8  # 타임 번호를 실제 시간으로 변환 (8시부터 시작)
        class_datetime = class_date.replace(hour=class_time, minute=0)
        return class_datetime < current_datetime

    def __str__(self):
        return f"{self.session_id:<8} {self.date:<10} {self.instructor_name:<8} {self.time:<6} {self.capacity:<6} {len(self.enrolled_user_ids):<6}"
class MemberSystem:
    def __init__(self, user_id, username, current_datetime: datetime):
        self.user_id = user_id
        self.username = username
        self.current_datetime = current_datetime
        self.teachers_name = {instructor.id: instructor.name for instructor in load_instructor_data()}
        self.class_list = self.load_classes_from_csv()
        self.enrolled_classes = set()
    
    def load_classes_from_csv(self):
        class_list = []
        reservations = read_csv(RESERVATION_PATH)
        
        for row in reservations:
            raw_users = row['수강 회원 id 리스트'].strip().strip('"')
            user_ids = [uid.strip() for uid in raw_users.split(",")] if raw_users else []
            class_list.append(ClassSession(
                session_id=row['아이디'].strip(),
                date=row['날짜'].strip(),
                time=row['타임'].strip(),
                teacher_id=row['강사 id'].strip(),
                enrolled_user_ids=user_ids,
                capacity=int(row['정원'].strip()),
                instructor_names=self.teachers_name
            ))
        return class_list

    def show_menu(self):
        while True:
            print("───────────────────────────────────────────────")
            print("1. 수업 신청\n2. 수업 취소 신청\n3. 신청 수업 조회\n4. 사물함 신청\n5. 사물함 연장\n6. 로그아웃")
            print("───────────────────────────────────────────────")
            choice = input("숫자를 입력해주세요 >> ")

            # 공백 검사 + 숫자 검사 + 범위 검사
            if not re.fullmatch(r'[1-6]', choice):
                print("[오류] 1~6 숫자만 가능합니다")
                continue

            if choice == "1":
                self.apply_class()
            elif choice == "2":
                self.request_cancellation(self.user_id, self.username)
            elif choice == "3":
                self.view_enrollments()
            elif choice == "4":
                self.apply_for_locker()
            elif choice == "5":
                self.extend_locker()
            elif choice == "6":
                print("로그아웃되었습니다.")
                break

    def display_classes(self):
        print("───────────────────────────────────────────────")
        print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
        print("───────────────────────────────────────────────")
        for c in self.class_list:
            print(c.__str__())
        print("───────────────────────────────────────────────")

    def apply_class(self):
        while True: 
            self.display_classes()
            session_id = input("신청하고 싶은 수업 ID를 입력해주세요 >> ")

            # 공백 검사 + 4자리 숫자 검사
            if not re.fullmatch(r'^\d{4}$', session_id):
                print("[오류] 수업 ID 형식에 맞지 않습니다.")
                continue
                
            target = next((c for c in self.class_list if c.session_id == session_id), None)
            if not target:
                print("[오류] 해당하는 수업 ID가 존재하지 않습니다.")
            elif target.is_past(self.current_datetime):
                print("[오류] 이미 지난 수업입니다.")
            elif self.user_id in target.enrolled_user_ids:
                print("[오류] 이미 신청된 수업입니다.")
            elif target.is_full():
                print("[오류] 수강이 마감된 수업입니다.")
            else: 
                target.enrolled_user_ids.append(self.user_id)
                self.save_classes_to_csv(RESERVATION_PATH)
                print("신청 완료되었습니다.")
                break

    def cancel_class(self):
        applied_classes = [c for c in self.class_list if self.username in c.enrolled_user_ids]
        if not applied_classes:
            print("[오류] 신청한 수업이 없습니다.")
            return

        print("───────────────────────────────────────────────")
        print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
        for c in applied_classes:
            print(c.__str__())
        print("───────────────────────────────────────────────")

        session_id = input("취소할 수업 ID를 입력해주세요 >> ")

        # 공백 검사 + 4자리 숫자 검사
        if not re.fullmatch(r'^\d{4}$', session_id):
            print("[오류] 수업 ID 형식에 맞지 않습니다.")
            return
            
        target = next((c for c in applied_classes if c.session_id == session_id), None)
        if not target:
            print("[오류] 신청한 수업이 아닙니다.")
            return

        target.enrolled_user_ids.remove(self.username)
        self.save_classes_to_csv(RESERVATION_PATH) 
        print("취소되었습니다.")
        return

    def view_enrollments(self):
        print("신청된 수업")
        print("───────────────────────────────────────────────")
        print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
        found_enrolled = False
        for c in self.class_list:
            if self.user_id in c.enrolled_user_ids:
                print(c.__str__())
                found_enrolled = True
        print("───────────────────────────────────────────────")

        # 취소 대기 중인 수업
        cancellations = read_csv(CANCELLATION_PATH)
        user_cancellations = [cancel for cancel in cancellations if cancel['user_id'].strip() == self.user_id]
        found_cancelled = False
        
        if user_cancellations:
            print("취소 대기 중인 수업")
            print("───────────────────────────────────────────────")
            print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
            print("───────────────────────────────────────────────")
            for cancel in user_cancellations:
                class_id = cancel['class_id'].strip()
                target_class = next((c for c in self.class_list if c.session_id == class_id), None)
                if target_class:
                    print(target_class.__str__())
                    found_cancelled = True
            print("───────────────────────────────────────────────")
        
        if not found_enrolled and not found_cancelled:
            print("[오류] 신청되거나 취소 대기중인 수업이 없습니다.")
        
        input("아무 키나 누르면 메뉴 화면으로 돌아갑니다 >> ")

    def save_classes_to_csv(self, path):
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['아이디', '날짜', '타임', '강사 id', '정원', '수강 회원 id 리스트']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for c in self.class_list:
                writer.writerow({
                    '아이디': c.session_id,
                    '날짜': c.date,
                    '타임': f"{c.time:02}",  # 항상 두 자리 시간으로
                    '강사 id': c.teacher_id,
                    '정원': c.capacity,
                    '수강 회원 id 리스트': ",".join(c.enrolled_user_ids)
                })
    
    def apply_for_locker(self):
        print("───────────────────────────────────────")
        print("[ 사물함 신청 ]")
        print("───────────────────────────────────────")

        locker_system = LockerSystem()

        # 1. 현재 회원이 이미 사물함을 사용 중인지 확인
        existing_locker = locker_system.get_user_locker(self.user_id)
        if existing_locker:
            expire_date = datetime.strptime(existing_locker.expire_date, "%y%m%d").date()
            remaining_days = (expire_date - self.current_datetime.date()).days
            print(f"[오류] 이미 {existing_locker.id}번 사물함 이용 중입니다.\n남은 일수: {remaining_days}일")
            return

        # 2. 신청일 포함 7일간 수업 예약이 2타임 이상인지 확인
        today = self.current_datetime.date()
        week_later = today + timedelta(days=6)

        reservation_count = 0
        for session in self.class_list:
            try:
                session_date = datetime.strptime(session.date, "%y%m%d").date()
            except ValueError:
                continue  # 날짜 파싱이 실패한 경우 무시

            if today <= session_date <= week_later:
                if self.user_id in session.enrolled_user_ids:
                    reservation_count += 1

        if reservation_count < 2:
            print("[오류] 사물함 신청은 신청일 기준 일주일에 2타임 이상 수업 예약이 있는 회원만 가능합니다.")
            return

        # 3. 빈 사물함이 존재하는지 확인하고 배정 시도
        success, message = locker_system.assign_locker(self.user_id, self.current_datetime.date())
        if success:
            print(f"{message}")
        else:
            if '\n' in message:
                main_msg, detail_msg = message.split('\n', 1)
                print(f"[오류] {main_msg}")
                print(detail_msg)
            else:
                print(f"[오류] {message}")
            
    def extend_locker(self):
        print("───────────────────────────────────────")
        print("[ 사물함 연장 신청 ]")
        print("───────────────────────────────────────")

        locker_system = LockerSystem()
        today = self.current_datetime.date()

        success, message = locker_system.extend_locker(self.user_id, today)
        if success:
            print(message)
        else:
            print(f"[오류] {message}")

    def request_cancellation(self, user_id, user_name) -> int:
        # CSV 파일에서 데이터 읽기
        reservations = read_csv(RESERVATION_PATH)
        cancellations = read_csv(CANCELLATION_PATH)
        
        # 사용자가 신청한 수업 ID와 수업 데이터 찾기
        reservations_class_id = [] # 해당 회원이 등록한 수업 ID 리스트
        user_reservations = [] # 해당 회원이 등록한 수업 객체 리스트

        for row in reservations:
            raw_users = row['수강 회원 id 리스트'].strip().strip('"')
            user_ids = [uid.strip() for uid in raw_users.split(",")] if raw_users else []
            if user_id in user_ids:
                reservations_class_id.append(row['아이디'].strip())
                user_reservations.append(row)
        
        # 이미 취소 신청한 수업 ID 찾기
        cancellations_class_id = [] # 해당 회원이 취소 신청한 수업 ID 리스트
        for row in cancellations:
            if row['user_id'].strip() == user_id:
                cancellations_class_id.append(row['class_id'].strip())
        
        # 취소 가능한 수업 ID 찾기
        available_class_id = [cid for cid in reservations_class_id if cid not in cancellations_class_id]
        
        # 취소 가능한 수업 데이터 찾기
        available_reservations = [] # 해당 회원이 취소 신청할 수 있는 수업 객체 리스트
        for row in user_reservations:
            if row['아이디'].strip() in available_class_id:
                available_reservations.append(row)
        
        # 취소 가능한 수업 목록 출력
        print("───────────────────────────────────────────────")
        print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
        print("───────────────────────────────────────────────")
        for row in available_reservations:
            raw_users = row['수강 회원 id 리스트'].strip().strip('"')
            user_ids = [uid.strip() for uid in raw_users.split(",")] if raw_users else []
            teacher_name = self.teachers_name.get(row['강사 id'].strip(), "Unknown")
            print(f"{row['아이디'].strip():<8} {row['날짜'].strip():<10} {teacher_name:<8} {row['타임'].strip():<6} {row['정원'].strip():<6} {len(user_ids):<6}")
        print("───────────────────────────────────────────────")
        
        # 취소할 수업 ID 입력 받기
        cr_class_id = input("취소 신청할 수업 ID를 입력해주세요 >> ")
        
        # 1. 수업 ID 형식 검사
        if not re.fullmatch(r'^\d{4}$', cr_class_id):
            print("[오류] 수업 ID 형식에 맞지 않습니다.")
            return -1
        
        # 2. 화면에 출력된 수업 ID인지 확인
        if cr_class_id not in reservations_class_id:
            print("[오류] 신청한 수업이 아닙니다.")
            return -2
        
        # 3. 이미 취소 신청한 수업인지 확인
        if cr_class_id not in available_class_id:
            print("[오류] 해당 수업은 이미 취소 신청 중입니다.")
            return -3
        
        # 취소 신청 데이터 추가
        cr = {
            'cancellation_id': str(len(cancellations) + 1),
            'class_id': cr_class_id,
            'user_id': user_id,
            'user_name': user_name
        }
        cancellations.append(cr)
        
        # CSV 파일에 저장
        write_csv(CANCELLATION_PATH, cancellations)
        
        print("취소 신청이 완료되었습니다.")
        return 0