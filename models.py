from dataclasses import dataclass

@dataclass
class Member:
    id : str
    pw : str
    name : str
    ph : str

@dataclass
class Instructor:
    id : str
    pw : str
    name : str
    ph : str

@dataclass
class Locker:
    id: str
    user_id: str
    expire_date: str  # YYMMDD 형식
    locker_status: str  # 'empty', 'occupied', 'removed'
    extended: bool = False  # 연장 여부

    def is_empty(self) -> bool:
        return self.user_id == ""