from models import Member, Instructor
from constants import SUCCESS
import utils
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import views
import file_handler


def login(user_type: str):
    member_list = file_handler.load_member_data()
    instructor_list = file_handler.load_instructor_data()

    while True: 
        views.print_login()
        id = views.prompt_id()

        if user_type == Member:
            user_list = member_list
        elif user_type == Instructor:
            user_list = instructor_list
            
        res, user = utils.validate_login_id(id, user_list)

        if res == SUCCESS:
            break
        print("[오류] 존재하지 않는 아이디입니다.\n")

    while True:
        views.print_login()
        pw = views.prompt_pw()

        if user.pw == pw:
            break
        print("[오류] 비밀번호가 맞지 않습니다.")
   
    return user
        