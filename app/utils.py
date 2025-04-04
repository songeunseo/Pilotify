def validate_date(date_str):
    """날짜 유효성 검사"""
    pass

def validate_time_slot(time_str):
    """타임 슬롯 유효성 검사"""
    pass

def validate_student_count(count):
    """수강 인원 수 유효성 검사"""
    pass

def return_to_menu(input_str):
    """메뉴 복귀 키워드 검사 ('m' 또는 'main')"""
    return input_str.lower() in ['m', 'main']