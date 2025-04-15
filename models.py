from dataclasses import dataclass
from datetime import datetime, date, time

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
    def __init__(self, datetime_str: str):
        """
        datetime_str: 'YYMMDD,HH:MM'
        """
        # 전체 datetime 문자열로 합쳐서 파싱
        self._datetime_obj: datetime = datetime.strptime(datetime_str, "%y%m%d,%H:%M")
    
    @property
    def datetime_obj(self) -> datetime:
        return self._datetime_obj
    
    def get_date(self) -> date:
        return self._datetime_obj.date()
    
    def get_time(self) -> time:
        return self._datetime_obj.time()
    
    def __str__(self) -> str:
        return self._datetime_obj.strftime("%Y-%m-%d %H:%M")