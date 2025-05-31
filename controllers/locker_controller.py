import csv
from datetime import datetime, timedelta, date
import re
from typing import List
from models import Locker
from utils import has_minimum_reservations
from constants import LOCKER_PATH, MAX_LOCKERS
from file_handler import read_csv, write_csv


class LockerSystem:
    def __init__(self):
        self.lockers = self.load_lockers()
    
    def load_lockers(self) -> List[Locker]:
        """사물함 데이터를 로드합니다."""
        try:
            # 파일이 비어있거나 헤더만 있는 경우 빈 리스트 반환
            data = read_csv(LOCKER_PATH)
            if not data: # 데이터 행이 없는 경우
                return []
            return [
                    Locker(
                        id=row['id'],
                        user_id=row['user_id'],
                        expire_date=row.get('expire_date', ""),  # 예외 없애기 위해 .get 사용
                        locker_status=row.get('locker_status', "empty"),  # 기본값 empty
                        extended=(row.get('extended', 'False') == 'True')
                        )
                        for row in data
                    ]
        except FileNotFoundError:
            # 파일이 없으면 빈 리스트 반환
            return []
        except Exception as e:
            print(f"[오류] 사물함 데이터를 읽는 중 오류 발생: {e}")
            return []
    
    def save_lockers(self):
        """사물함 데이터를 저장합니다."""
        data = [{
    'id': l.id,
    'user_id': l.user_id,
    'expire_date': l.expire_date,
    'locker_status': l.locker_status,
    'extended': str(l.extended)
} for l in self.lockers]
        try:
            write_csv(LOCKER_PATH, data)
        except Exception as e:
             print(f"[오류] 사물함 데이터를 저장하는 중 오류 발생: {e}")

    def get_remaining_days(self, current_datetime:datetime, locker: Locker) -> int:
        """남은 일수를 반환합니다."""
        expire_date = datetime.strptime(locker.expire_date, "%y%m%d")
        remaining_days = current_datetime-expire_date

        if(remaining_days< timedelta(days=0)):
            locker.user_id = ""
        
        self.save_lockers()
        return remaining_days.days
    
    def print_locker_status(self, current_datetime: datetime) -> None:
        print("───────────────────────────────────────")
        print("사물함 번호 | 회원  | 남은 기간 | ")
        print("───────────────────────────────────────")
        
        for l in self.lockers:
            remaining_days = self.get_remaining_days(current_datetime=current_datetime, locker=l) if l.user_id!="" else "-"
            user_id = l.user_id if l.user_id != "" else "-"
            print(f"{l.id}  {user_id}  {remaining_days}")
        print("───────────────────────────────────────")

    def is_occupied(self, id: str) -> bool:
        """사물함이 사용중인지 반환합니다."""
        return bool(next((l.user_id for l in self.lockers if l.id == id), None))
    
    
    def get_empty_locker_count(self) -> int:
        """비어있는 사물함 개수를 반환합니다."""
        return sum(1 for l in self.lockers if l.is_empty())
    
    def get_used_locker_count(self) -> int:
        """사용 중인 사물함 개수를 반환합니다."""
        return len(self.lockers) - self.get_empty_locker_count()
    
    def get_user_locker(self, user_id: str) -> Locker | None:
        """사용자의 사물함을 찾습니다."""
        return next((l for l in self.lockers if l.user_id == user_id and not l.is_empty()), None)
    
    def set_locker_count(self, new_count_str: str) -> tuple[bool, str]:
        """사물함 개수를 설정합니다."""
        # 1. 입력값이 0 이상의 정수인지 검사
        if not re.fullmatch(r'^\d+$', new_count_str):
            return False, "입력 형식에 맞지 않습니다."
        
        new_count = int(new_count_str)
        # 음수 검사는 이미 정규식에서 걸러짐
        
        current_count = len(self.lockers)
        current_used = self.get_used_locker_count()

        # 2. 최대 개수(25) 초과 시
        if new_count > MAX_LOCKERS:
            return False, f"사물함 개수는 최대 {MAX_LOCKERS}개까지 설정 가능합니다."
        
        # 3. 사용 중인 사물함보다 적게 입력 시
        if new_count < current_used:
            return False, f"빈 사물함이 부족하여 최소 {current_used}개까지만 축소 가능합니다."
        
        # 4. 정상 처리
        # 현재 사물함 개수보다 늘리는 경우
        if new_count > current_count:
            # 부족한 만큼 빈 사물함 추가
            for i in range(current_count, new_count):
                # 사물함 ID는 1부터 시작, 0 채움 2자리
                self.lockers.append(Locker(
                id=f"{i+1:02d}",
                user_id="",
                expire_date="",
                locker_status="empty",
                extended=False
            ))

        # 현재 사물함 개수보다 줄이는 경우
        elif new_count < current_count:
            # 뒤에서부터 빈 사물함만 삭제
            # current_used 체크로 사용 중인 사물함은 new_count 범위 안에 남게 됨
            # 리스트 슬라이싱으로 new_count 개수만큼 남김
            self.lockers = self.lockers[:new_count]
        
        # 사물함 ID 재정렬 (혹시 모르니) - 필요 없을 수도 있지만 안전하게
        # for i, locker in enumerate(self.lockers):
        #     locker.id = f"{i+1:02d}"

        self.save_lockers()
        return True, f"사물함 개수 {new_count}개로 변경 완료되었습니다."
    
    def assign_locker(self, user_id: str, today: date) -> tuple[bool, str]:
        existing_locker = self.get_user_locker(user_id)
        if existing_locker:
            expire_date = datetime.strptime(existing_locker.expire_date, "%y%m%d").date()
            remaining = (expire_date - today).days
            return False, f"이미 {existing_locker.id}번 사물함을 이용 중입니다.\n남은 일수: {remaining}일"
        
        empty_lockers = sorted([l for l in self.lockers if l.is_empty()], key=lambda x: x.id)
        if not empty_lockers:
            return False, "남은 사물함이 없습니다."

        # 수업 예약 조건 확인
        check_end = today + timedelta(days=6)
        if not has_minimum_reservations(user_id, today, check_end):
            return False, "사물함 신청은 신청일 기준 일주일에 2타임 이상 수업 예약이 있는 회원만 가능합니다."

        # 필드 업데이트
        empty_locker = empty_lockers[0]
        empty_locker.user_id = user_id
        empty_locker.expire_date = (today + timedelta(days=6)).strftime("%y%m%d")
        empty_locker.locker_status = "occupied"
        self.save_lockers()
        return True, f"{empty_locker.id}번 사물함이 배정되었습니다."
    
    def release_locker(self, user_id: str):
        locker = self.get_user_locker(user_id)
        if locker:
            locker.user_id = ""
            locker.expire_date = ""
            locker.locker_status = "empty"
            locker.extended = False  # 연장 상태 초기화
            self.save_lockers()
    
    def expire_lockers(self, today: date) -> None:
        expired_lockers = []
        
        # 1단계: 만료 대상 식별
        for locker in self.lockers:
            if locker.locker_status != "occupied":
                continue
                
            try:
                expire_date = datetime.strptime(locker.expire_date, "%y%m%d").date()
            except ValueError:
                expired_lockers.append(locker)
                continue
                
            if expire_date < today:
                expired_lockers.append(locker)

        # 2단계: 직접 필드 초기화
        for locker in expired_lockers:
            self.release_locker(locker.user_id)  
    
        if expired_lockers:
            self.save_lockers()  # 변경사항 저장

    def extend_locker(self, user_id: str, today: date) -> tuple[bool, str]:
        locker = self.get_user_locker(user_id)
        if not locker:
            return False, "현재 사용 중인 사물함이 없습니다."
        
        if locker.extended:
            return False, "이미 연장된 사물함은 추가 연장이 불가능합니다."
        
        # 예약 조건 검증
        expire_date = datetime.strptime(locker.expire_date, "%y%m%d").date()

        check_start = expire_date + timedelta(days=1)
        check_end = check_start + timedelta(days=6)
        if not has_minimum_reservations(user_id, check_start, check_end):
            return False, "연장은 사물함 기존 종료일 이후 7일 동안 수업 예약이 2타임 이상 있어야 가능합니다."
        
        # 7일 연장 처리
        new_expire = expire_date + timedelta(days=7)
        locker.expire_date = new_expire.strftime("%y%m%d")
        locker.extended = True
        remaining = (new_expire - today).days
        self.save_lockers()
        return True, f"{locker.id}번 사물함 사용 기간이 연장되었습니다.\n남은 일수: {remaining}일"
