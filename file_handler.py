import csv
from constants import MEMBER_PATH, INSTRUCTOR_PATH
from models import Member, Instructor

def load_member_data() -> list[Member]:
    member_data=[]
    with open(MEMBER_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            member = Member(
                id = row['아이디'],
                pw = row['비밀번호'],
                name = row['이름'],
                ph = row['전화번호'], 
            )   
            member_data.append(member)
    return member_data

def load_instructor_data() -> list[Instructor]:
    instructor_data = []
    with open(INSTRUCTOR_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instructor = Instructor(
                id=row['아이디'],
                pw=row['비밀번호'],
                name=row['이름'],
                ph=row['전화번호']
            )
            instructor_data.append(instructor)
    return instructor_data
    

def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(filepath, data):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        if not data:
            # 데이터가 비어있는 경우 기본 헤더만 작성
            writer = csv.DictWriter(f, fieldnames=["cancellation_id", "class_id", "user_id", "user_name"])
            writer.writeheader()
        else:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

