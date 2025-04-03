from app import views
from app.controllers import member_controller
from app.models import Member

def Main():
    while True: 
        views.print_welcome()

        ## 로그인하거나 회원가입
        choice = views.print_login_or_register()

        ## 로그인 후 메인 메뉴로 진입

        ## 회원 가입
