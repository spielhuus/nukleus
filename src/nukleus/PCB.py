from typing import Dict

class PCB():
    def __init__(self):
        self.elements = []
        self.paper: str = ""

        self.title: str = ""
        self.date: str = ""
        self.company: str = ""
        self.rev: str = ""
        self.comment: Dict[int, str] = {}
