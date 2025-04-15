from dataclasses import dataclass
from datetime import datetime

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

class CurrentDateTime:
    def __init__(self, date_str: str, time_str: str):
        """
        date_str: 'YYYY-MM-DD'
        time_str: 'HH:MM'
        """
        # 전체 datetime 문자열로 합쳐서 파싱
        combined = f"{date_str} {time_str}"
        self._datetime_obj: datetime = datetime.strptime(combined, "%Y-%m-%d %H:%M")
    
    @property
    def datetime_obj(self) -> datetime:
        return self._datetime_obj
    
    def get_date(self) -> str:
        return self._datetime_obj.strftime("%Y-%m-%d")
    
    def get_time(self) -> str:
        return self._datetime_obj.strftime("%H:%M")
    
    def __str__(self) -> str:
        return self._datetime_obj.strftime("%Y-%m-%d %H:%M")