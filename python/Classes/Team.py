from typing import Dict


class Team:
    def __init__(self, data: Dict):
        self.id = int(data["id"])
        self.name = data["name"]
        self.score = data["score"]
