class Event:
    def __init__(self, desc: str, index: int, is_hit: bool = False):
        self.desc = desc
        self.index = index
        self.is_hit = is_hit
