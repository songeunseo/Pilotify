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