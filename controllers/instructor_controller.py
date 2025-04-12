import datetime as dt
from models import Instructor

def register_class():
    # if :
    #     print("")
    # elif :
    #     print("[수업 등록]")
    #     day = input()
    #     day
        return 0

def check_class():
    return 0

def instructor_menu(instructor: Instructor):

    while True:
        i = input()
        if i == 1:
            register_class()
        elif i == 2:
            check_class()
        elif i == 3:
            print("로그아웃합니다.")
            break