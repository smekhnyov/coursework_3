class Settings:

    def __init__(self, save: int = 2, dist: int = 2):
        self.save = save
        self.dist = dist

    def get_save(self) -> int:
        return self.save

    def get_dist(self) -> int:
        return self.dist

    def set_save(self, save) -> None:
        self.save = save

    def set_dist(self, dist) -> None:
        self.dist = dist

