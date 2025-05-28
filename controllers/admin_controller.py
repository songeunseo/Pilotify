import re
from utils import read_csv, write_csv
from constants import *
from datetime import datetime

def set_instructor_code(current_datetime:datetime)->None:
    rows = read_csv(INST_CODE_PATH)
    if not rows:
        last_modified_date = f"{current_datetime:%y%m%d}"
        current_code = "0000"
        write_csv(INST_CODE_PATH, [{"last_modified_date": last_modified_date, "current_code": current_code}])
    else:
        last_modified_date = rows[0]["last_modified_date"]
        current_code = rows[0]["current_code"]

    print("───────────────────────────────────────")
    print("[ 강사 인증 코드 설정 ]")
    print("───────────────────────────────────────")
    print(f"현재 인증 코드: {current_code}")
    new_code = input("새로운 인증 코드를 입력하세요 (4자리 숫자) >> ")

    if not re.fullmatch(r"^\d{4}$", new_code):
        print("[오류] 올바른 인증코드가 아닙니다.")
        return
    if new_code == current_code:
        print("[오류] 현재 인증 코드와 동일한 값으로는 변경할 수 없습니다.")
        return
    if f"{current_datetime:%y%m}" == last_modified_date[:4]:
        next_month = current_datetime.month + 1
        next_year = current_datetime.year
        if next_month > 12: next_month = 1; next_year += 1
        print(f"[오류] 이번 달에는 이미 인증 코드를 변경했습니다. 다음 변경 가능 시점: {next_year}년 {next_month}월 1일부터")
        return

    write_csv(INST_CODE_PATH, [{"last_modified_date": f"{current_datetime:%y%m%d}", "current_code": new_code}])
    print("인증 코드가 정상적으로 변경되었습니다.")
    return