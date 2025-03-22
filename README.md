# Pilotify
2025년 1학기 전공기초프로젝트 프로젝트 / 필라테스 예약 관리 시스템

## 📌 프로젝트 구조

```
Pilotify/
│
├── app/
│   ├── __init__.py               # 애플리케이션 초기화
│   ├── main.py                   # 메인 실행 파일
│   ├── auth.py                   # 로그인, 회원가입 관련 처리
│   ├── models.py                 # 데이터 모델 (회원, 강사, 수업 등)
│   ├── views.py                  # 화면 출력/입력 처리
│   ├── controllers/              # 각 기능별 처리 로직
│   │   ├── __init__.py
│   │   ├── instructor_controller.py # 강사 관련 기능
│   │   ├── member_controller.py    # 회원 관련 기능
│   │   └── reservation_controller.py # 예약 관련 기능
│   ├── utils.py                  # 유틸리티 함수 (날짜 처리, 입력 검증 등)
│   └── file_handler.py           # 파일 읽기/쓰기 관련 처리
│
├── data/
│   ├── members.txt              # 회원 정보 저장 (TXT 파일)
│   ├── instructors.txt          # 강사 정보 저장 (TXT 파일)
│   └── reservations.csv         # 예약 정보 저장 (CSV 파일)
│
├── requirements.txt             # 프로젝트 의존성 목록
├── README.md                    # 프로젝트 설명 파일
└── config.py                    # 설정 파일 (디폴트 값, 설정 값 등)
```
