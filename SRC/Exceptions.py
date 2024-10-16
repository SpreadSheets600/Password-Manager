class DatabaseError(Exception):
    def __init__(self, message="Database Error Occurred"):
        self.message = message
        super().__init__(self.message)
