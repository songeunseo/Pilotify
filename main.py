import views
import utils
from constants import SUCCESS, USER_TYPE_INSTRUCTOR, USER_TYPE_MEMBER, USER_TYPE_ADMIN
from auth.signup import signup
from auth.login import login
from datetime import datetime
from controllers.member_controller import MemberSystem
from controllers.instructor_controller import show_instructor_menu
from controllers.admin_controller import show_admin_menu
from controllers.locker_controller import LockerSystem
import re

def main():
    ## 제목 출력
    views.print_title()
    views.prompt_menu_choice()
      
    while True:
        ## 날짜와 시간 입력
        views.print_date_time()
        datetime_str = views.prompt_date_time()
        
        ## 입력 처리
        datetime_check = utils.validate_datetime_input(datetime_str)
        if datetime_check != SUCCESS: 
            print("[오류] 날짜 시간 규칙에 맞지 않습니다.")
            continue

        ## 날짜와 시간 저장
        current_datetime = datetime.strptime(datetime_str, "%y%m%d,%H:%M")
        break
            
    while True: 
        locker_system = LockerSystem()
        locker_system.expire_lockers(current_datetime.date())
        while True: 
          ## 회원 혹은 강사를 선택
          views.print_main_menu()
          main_choice = views.prompt_menu_choice()

          if re.fullmatch(r'[1-4]', main_choice):
            break
          print("[오류] 1~4 숫자만 가능합니다.")

        if main_choice == "1":
           user_type = USER_TYPE_MEMBER
        elif main_choice == "2":
           user_type = USER_TYPE_INSTRUCTOR
        elif main_choice == "3":
           user_type = USER_TYPE_ADMIN
        else:
          break

        
        if user_type != USER_TYPE_ADMIN:
          while True: 
            ## 회원가입 혹은 로그인을 선택
            views.print_register_login_menu()
            register_login_choice = views.prompt_menu_choice()
            if re.fullmatch(r'[1-3]', register_login_choice):
              break
            print("[오류] 1~3 숫자만 가능합니다.")


          ## 회원가입
          if register_login_choice == "1":
            user = signup(user_type)

          ## 로그인 
          elif register_login_choice == "2":
            user = login(user_type)

          ## 시작 메뉴로 돌아가기
          else:
            continue

        else:
           res = login(user_type)
           show_admin_menu(current_datetime)

        ## 강사 화면
        if user_type == USER_TYPE_INSTRUCTOR:
          show_instructor_menu(user, current_datetime) # type: ignore

        ## 회원 화면
        elif user_type == USER_TYPE_MEMBER:
           system = MemberSystem(user.id, user.name, current_datetime)
           system.show_menu()            
           
           
if __name__ == '__main__':
    main()