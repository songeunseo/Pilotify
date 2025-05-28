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
            # 파일이 비어있거나 헤더만 있는 경우 빈 리스트 반환
            with open(LOCKER_PATH, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
                if not data: # 데이터 행이 없는 경우
                    return []
                return [Locker(id=row['id'], user_id=row['user_id']) for row in data]
        except FileNotFoundError:
            # 파일이 없으면 빈 리스트 반환
            return []
        except Exception as e:
            print(f"[오류] 사물함 데이터를 읽는 중 오류 발생: {e}")
            return []
    
    def save_lockers(self):
        """사물함 데이터를 저장합니다."""
        data = [{'id': l.id, 'user_id': l.user_id} for l in self.lockers]
        try:
            write_csv(LOCKER_PATH, data, fieldnames=['id', 'user_id'])
        except Exception as e:
             print(f"[오류] 사물함 데이터를 저장하는 중 오류 발생: {e}")

    
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
                self.lockers.append(Locker(id=f"{i+1:02d}", user_id=""))

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
    
    def assign_locker(self, user_id: str) -> tuple[bool, str]:
        """사용자에게 사물함을 할당합니다. (회원당 1개 제한 포함)"""
        # 1. 이미 사물함을 사용 중인지 확인
        if self.get_user_locker(user_id):
            return False, "이미 사물함을 사용 중입니다. (회원당 1개 제한)"
        
        # 2. 빈 사물함 찾기
        empty_locker = next((l for l in self.lockers if l.is_empty()), None)
        if not empty_locker:
            return False, "사용 가능한 사물함이 없습니다."
        
        # 3. 사물함 할당 및 저장
        empty_locker.user_id = user_id
        self.save_lockers()
        return True, f"사물함 {empty_locker.id}번이 할당되었습니다."
    
    def release_locker(self, user_id: str) -> tuple[bool, str]:
        """사용자의 사물함을 해제합니다."""
        # 1. 사용자의 사물함 찾기
        locker = self.get_user_locker(user_id)
        if not locker:
            return False, "사용 중인 사물함이 없습니다."
        
        # 2. 사물함 해제 및 저장
        locker.user_id = ""
        self.save_lockers()
        return True, f"사물함 {locker.id}번이 해제되었습니다."
