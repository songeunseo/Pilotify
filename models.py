@dataclass
class Locker:
    id: str  # 사물함 번호
    user_id: str  # 사용 중인 회원 아이디 (비어있으면 "")
    
    def is_empty(self) -> bool:
        return self.user_id == "" 