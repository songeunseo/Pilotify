class ClassTime:
    """수업 시간대(타임) 클래스"""
    AVAILABLE_TIMES = [
        "09:00", "10:30", "12:00", "13:30", 
        "15:00", "16:30", "18:00", "19:30"
    ]

class Class:
    """수업 클래스"""
    def __init__(self, date, time_slot, max_students, instructor_id):
        self.date = date
        self.time_slot = time_slot
        self.max_students = max_students
        self.instructor_id = instructor_id
        self.enrolled_students = []  # 등록된 회원 리스트

class Instructor:
    """강사 클래스"""
    def __init__(self, name, id, phone):
        self.name = name
        self.id = id
        self.phone = phone