from app.constants import SUCCESS, BASIC_ERROR
from datetime import datetime

def validate_datetime_input(user_input: str) -> int:
    # 콤마가 정확히 한 개여야 함, 공백이 없어야 함
    if (user_input.count(',') != 1) or (' ' in user_input):
        return BASIC_ERROR

    date_str, time_str = user_input.split(',')

    # 날짜는 6자리, 시간은 5자리 + ':' 포함
    if (len(date_str) != 6) or (len(time_str) != 5 or ':' not in time_str):
        return BASIC_ERROR

    # 실제 존재하는 날짜/시간인지 확인
    try:
        datetime.strptime(date_str + ' ' + time_str, "%y%m%d %H:%M")
    except ValueError:
        return BASIC_ERROR

    return SUCCESS

def validate_menu_choice(user_input: str, valid_choices: list[str]) -> bool:
    # 입력이 숫자이고, 선택지 안에 있는지 검사
    if user_input.isdigit() and user_input in valid_choices:
        return SUCCESS
    return BASIC_ERROR