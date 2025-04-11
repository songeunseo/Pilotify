# Pilotify
2025년 1학기 전공기초프로젝트 프로젝트 / 필라테스 예약 관리 시스템

## 🤝 협업 규칙

- `main` 브랜치는 보호되어 있어 직접 push 시도 시 거부됨
- 모든 작업은 **새 브랜치 생성 → Pull Request로 병합**
- PR은 리뷰 없이도 바로 머지 가능 (승인 생략)
- 커밋 메시지는 [Gitmoji](https://gitmoji.dev/) 스타일 또는 `feat:`, `fix:` 등 prefix 사용 권장

## 📌 프로젝트 구조

```
Pilotify/
│
├── auth/                        # 인증 관련 모듈
│   ├── login.py                 # 로그인 함수
│   └── signup.py                # 회원가입 함수
├── controllers/                 # 각 기능별 처리 로직
│   ├── __init__.py
│   ├── instructor_controller.py # 강사 관련 기능
│   ├── member_controller.py    # 회원 관련 기능
│   └── reservation_controller.py # 예약 관련 기능
│
├── data/                       # 데이터 저장 디렉토리
│   ├── members.csv            # 회원 정보 저장 (CSV 파일)
│   ├── instructors.csv        # 강사 정보 저장 (CSV 파일)
│   └── class.csv              # 수업 정보 저장 (CSV 파일)
│
├── __init__.py                # 패키지 초기화
├── main.py                    # 메인 실행 파일
├── models.py                  # 데이터 모델 (회원, 강사, 수업 등)
├── utils.py                   # 유틸리티 함수 (날짜 처리, 입력 검증 등)
├── views.py                   # 화면 출력/입력 처리
├── file_handler.py            # 파일 읽기/쓰기 관련 처리
├── config.py                  # 설정 파일 (디폴트 값, 설정 값 등)
├── requirements.txt           # 프로젝트 의존성 목록
└── README.md                  # 프로젝트 설명 파일
```
