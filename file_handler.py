import csv
from app.constants import MEMBER_PATH, INSTRUCTOR_PATH
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
                id=row['id'],
                pw=row['pw'],
                name=row['name'],
                ph=row['ph']
            )
            instructor_data.append(instructor)
    return instructor_data