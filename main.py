import views
from controllers import member_controller
from models import Member
import utils
from app.constants import SUCCESS, USER_TYPE_INSTRUCTOR, USER_TYPE_MEMBER
from auth.signup import signup
from auth.login import login
from controllers.instructor_controller import instructor_menu
# from controllers.member_controller import member_main


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
      date_str, time_str = datetime_str.split(',')
      
      ## 날짜와 시간 저장 필요
      
      if datetime_check == SUCCESS: 
        break
      print("[오류] 날짜 시간 규칙에 맞지 않습니다.")
            
    while True: 
        while True: 
          ## 회원 혹은 강사를 선택
          views.print_main_menu()
          main_choice = views.prompt_menu_choice()

          ## 입력 처리
          main_choice_check = utils.validate_menu_choice(main_choice, ["1", "2", "3"])

          if main_choice_check == SUCCESS:
             break
          print("[오류] 1~3 숫자만 가능합니다.")

        if main_choice == "1":
           user_type = USER_TYPE_MEMBER
        elif main_choice == "2":
           user_type = USER_TYPE_INSTRUCTOR
        else:
          break


        while True: 
          ## 회원가입 혹은 로그인을 선택
          views.print_register_login_menu()
          register_login_choice = views.prompt_menu_choice()

          ## 입력 처리
          register_login_choice_check = utils.validate_menu_choice(register_login_choice, ["1", "2", "3"])

          if register_login_choice_check == SUCCESS:
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
        

        ## 강사 화면
        if user_type == USER_TYPE_INSTRUCTOR:
          instructor_menu(user)

        ## 회원 화면
        # elif user_type == USER_TYPE_MEMBER:
        #    member_main(user)
           
if __name__ == '__main__':
    main()