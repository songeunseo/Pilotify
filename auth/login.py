from models import Member, Instructor
from constants import SUCCESS
import utils
import sys
import os
from constants import USER_TYPE_MEMBER, USER_TYPE_INSTRUCTOR, USER_TYPE_ADMIN

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import views
import file_handler


def login(user_type: str):
    member_list = file_handler.load_member_data()
    instructor_list = file_handler.load_instructor_data()

    while True: 
        views.print_login()
        id = views.prompt_id()

        if user_type == USER_TYPE_MEMBER:
            user_list = member_list
        elif user_type == USER_TYPE_INSTRUCTOR:
            user_list = instructor_list

        if user_type == USER_TYPE_ADMIN:
            if id == "Admin":
                break
            else:
                print("[오류] 틀린 아이디입니다.\n")
            
        else: 
            res, user = utils.validate_login_id(id, user_list)

            if res == SUCCESS:
                break
            else: 
                print("[오류] 존재하지 않는 아이디입니다.\n")

    while True:
        views.print_login()
        pw = views.prompt_pw()

        if user_type == USER_TYPE_ADMIN:
            if pw == "Admin@1234":
                user = None
                break
            else:
                print("[오류] 비밀번호가 맞지 않습니다.\n")
        else:
            if user.pw == pw:
                break
            else: 
                print("[오류] 비밀번호가 맞지 않습니다.")
    print("로그인이 완료되었습니다.")
    return user
        