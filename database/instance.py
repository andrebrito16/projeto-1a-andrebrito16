from database.database import Database


class DatabaseInstance:
    def __init__(self):
        self.instance = Database("getit")
