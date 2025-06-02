## 성공
SUCCESS = 0

## 기본 형식 위반
BASIC_ERROR = -1
## 조건 위반
GRAMMAR_ERROR = -2
## 중복 확인
NO_DUPLICATION = -3

## Member
USER_TYPE_MEMBER = 'm'  
## Instructor    
USER_TYPE_INSTRUCTOR = 'n'
## Admin
USER_TYPE_ADMIN = 'a'

##file_path
MEMBER_PATH = 'data/members.csv'
INSTRUCTOR_PATH = 'data/instructors.csv'
RESERVATION_PATH = 'data/reservations.csv'
CANCELLATION_PATH = 'data/request_cancel_class.csv'
DATETIME_PATH = 'data/datetime.csv'
INST_CODE_PATH = 'data/instructor_code.csv'

## Locker
LOCKER_PATH = 'data/lockers.csv'
MAX_LOCKERS = 25  # 최대 사물함 개수

## Instructor auth code
INSTRUCTOR_CODE = '0000'