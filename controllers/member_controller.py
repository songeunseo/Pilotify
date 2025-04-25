import csv
import os,sys
from file_handler import load_member_data, load_instructor_data
from datetime import datetime
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
    def __init__(self, username, current_datetime: datetime):
        self.username = username
        self.current_datetime = current_datetime
        self.teachers_name = {instructor.id: instructor.name for instructor in load_instructor_data()}
        self.class_list = self.load_classes_from_csv()
        self.enrolled_classes = set()
    
    def load_classes_from_csv(self):
        class_list = []
        with open("data/class.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
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
            print("1. 수업 신청\n2. 수업 취소\n3. 신청 수업 조회\n4. 로그아웃")
            print("───────────────────────────────────────────────")
            choice = input("숫자를 입력해주세요 >> ").strip()

            if choice == "1":
                self.apply_class()
            elif choice == "2":
                self.cancel_class()
            elif choice == "3":
                self.view_enrollments()
            elif choice == "4":
                print("로그아웃되었습니다.")
                break
            else:
                print("[오류] 1~4 숫자만 가능합니다")

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
            session_id = input("신청하고 싶은 수업 ID를 입력해주세요 >> ").strip()
            if not re.match(r'^\d{4}$', session_id):
                print("[오류] 수업 ID 형식에 맞지 않습니다.")
                continue
                
            target = next((c for c in self.class_list if c.session_id == session_id), None)
            if not target:
                print("[오류] 해당하는 수업 ID가 존재하지 않습니다.")
            elif target.is_past(self.current_datetime):
                print("[오류] 이미 지난 수업입니다.")
            elif self.username in target.enrolled_user_ids:
                print("[오류] 이미 신청된 수업입니다.")
            elif target.is_full():
                print("[오류] 수강이 마감된 수업입니다.")
            else: 
                target.enrolled_user_ids.append(self.username)
                self.save_classes_to_csv("data/class.csv")
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

        session_id = input("취소할 수업 ID를 입력해주세요 >> ").strip()
        if not re.match(r'^\d{4}$', session_id):
            print("[오류] 수업 ID 형식에 맞지 않습니다.")
            return
            
        target = next((c for c in applied_classes if c.session_id == session_id), None)
        if not target:
            print("[오류] 신청한 수업이 아닙니다.")
            return

        target.enrolled_user_ids.remove(self.username)
        self.save_classes_to_csv("data/class.csv") 
        print("취소되었습니다.")
        return

    def view_enrollments(self):
        print("───────────────────────────────────────────────")
        print(" 수업 ID |  날짜  |  이름  | 타임 |정원|신청 인원|")
        found = False
        for c in self.class_list:
            if self.username in c.enrolled_user_ids:
                print(c.__str__())
                found = True
        if not found:
            print("신청한 수업이 없습니다.")
        print("───────────────────────────────────────────────")
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
'''
if __name__ == "__main__":
    user_id = "park124"
    raw_date = "250409"
    raw_time = "23:59"

    if len(raw_date) != 6 or len(raw_time) != 5 or raw_time[2] != ':':
        print("[오류] 날짜 또는 시간 형식이 잘못되었습니다.")
        exit()

    hhmm = raw_time.replace(":", "")
    current_ymdhm = int(raw_date + hhmm)
    system = MemberSystem(user_id, current_ymdhm)
    system.show_menu()
'''