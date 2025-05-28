import csv
import re
from typing import List
from models import Locker
from constants import LOCKER_PATH, MAX_LOCKERS
from file_handler import read_csv, write_csv

class LockerSystem:
    def __init__(self):
        self.lockers = self.load_lockers()
    
    def load_lockers(self) -> List[Locker]:
        """사물함 데이터를 로드합니다."""
        try:
            data = read_csv(LOCKER_PATH)
            return [Locker(id=row['id'], user_id=row['user_id']) for row in data]
        except FileNotFoundError:
            # 파일이 없으면 빈 리스트 반환
            return []
    
    def save_lockers(self):
        """사물함 데이터를 저장합니다."""
        data = [{'id': l.id, 'user_id': l.user_id} for l in self.lockers]
        write_csv(LOCKER_PATH, data)
    
    def get_empty_locker_count(self) -> int:
        """비어있는 사물함 개수를 반환합니다."""
        return sum(1 for l in self.lockers if l.is_empty())
    
    def get_used_locker_count(self) -> int:
        """사용 중인 사물함 개수를 반환합니다."""
        return len(self.lockers) - self.get_empty_locker_count()
    
    def get_user_locker(self, user_id: str) -> Locker | None:
        """사용자의 사물함을 찾습니다."""
        return next((l for l in self.lockers if l.user_id == user_id), None)
    
    def set_locker_count(self, new_count: int) -> tuple[bool, str]:
        """사물함 개수를 설정합니다."""
        # 1. 입력값이 정수인지 검사
        if not re.fullmatch(r'^\d+$', str(new_count)):
            return False, "입력 형식에 맞지 않습니다."
        new_count = int(new_count)
        if new_count < 0:
            return False, "입력 형식에 맞지 않습니다."
        # 2. 최대 개수 초과 시
        if new_count > MAX_LOCKERS:
            return False, "사물함 개수는 최대 25개까지 설정 가능합니다."
        current_used = self.get_used_locker_count()
        # 3. 사용 중인 사물함보다 적게 입력 시
        if new_count < current_used:
            return False, f"빈 사물함이 부족하여 최소 {current_used}개까지만 축소 가능합니다."
        # 4. 정상 처리
        if new_count > len(self.lockers):
            for i in range(len(self.lockers), new_count):
                self.lockers.append(Locker(id=f"{i+1:02d}", user_id=""))
        elif new_count < len(self.lockers):
            # 뒤에서부터 빈 사물함만 삭제
            empty_count = self.get_empty_locker_count()
            can_remove = min(empty_count, len(self.lockers) - new_count)
            # 이미 위에서 current_used 체크로 걸러짐, 아래는 실제 삭제만 진행
            # 뒤에서부터 빈 사물함 삭제
            removed = 0
            for idx in range(len(self.lockers)-1, -1, -1):
                if removed >= len(self.lockers) - new_count:
                    break
                if self.lockers[idx].is_empty():
                    del self.lockers[idx]
                    removed += 1
        self.save_lockers()
        return True, f"사물함 개수 {new_count}개로 변경 완료되었습니다."
    
    def assign_locker(self, user_id: str) -> tuple[bool, str]:
        """사용자에게 사물함을 할당합니다."""
        # 이미 사물함을 사용 중인지 확인
        if self.get_user_locker(user_id):
            return False, "이미 사물함을 사용 중입니다."
        
        # 빈 사물함 찾기
        empty_locker = next((l for l in self.lockers if l.is_empty()), None)
        if not empty_locker:
            return False, "사용 가능한 사물함이 없습니다."
        
        empty_locker.user_id = user_id
        self.save_lockers()
        return True, f"사물함 {empty_locker.id}번이 할당되었습니다."
    
    def release_locker(self, user_id: str) -> tuple[bool, str]:
        """사용자의 사물함을 해제합니다."""
        locker = self.get_user_locker(user_id)
        if not locker:
            return False, "사용 중인 사물함이 없습니다."
        
        locker.user_id = ""
        self.save_lockers()
        return True, f"사물함 {locker.id}번이 해제되었습니다." 