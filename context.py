from typing import Optional
from models import CurrentDateTime

# 전역 상태 관리
current_datetime: Optional[CurrentDateTime] = None

def get_current_datetime() -> CurrentDateTime:
    """현재 날짜/시간을 반환합니다. 설정되지 않은 경우 에러를 발생시킵니다."""
    if current_datetime is None:
        raise RuntimeError("current_datetime이 설정되지 않았습니다. main()에서 먼저 설정해주세요.")
    return current_datetime 