from app import views
from app.models import Member

def member_menu(current_user: Member):
    ## 현재 멤버 이름을 넘겨받아 출력 가능

    ## 멤버 화면 출력
    views.print_member_menu()

    ## 각 번호를 통해 메뉴 진입

def show_available_class(current_user: Member):
    ## 등록된 수업 출력
    views.print_class_list()

    ## 키 입력으로 돌아가기
    return

def show_my_reservation(current_user: Member):
    ## 사용자가 수강하는 수업 출력
    views.print_reservation_history()

    ## 키 입력으로 돌아가기
    return

