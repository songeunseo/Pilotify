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