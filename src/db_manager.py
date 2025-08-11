import psycopg2

class DBManager:
    host: str
    database: str
    user: str
    password: str

    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
