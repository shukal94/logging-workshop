import sqlite3
import src.utils as utils


class BaseDbClient:
    schema: str

    def __init__(self, schema):
        self.schema = schema

    def connect(self):
        pass

    def get_cursor(self):
        pass

    def execute_script(self, script: str):
        pass

    def execute_statement(self, statement, parameters=(), fetch_one=False):
        pass

    def close(self):
        pass

    def close_cursor(self):
        pass

    def close_connection(self):
        pass


class SqliteClient(BaseDbClient):
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, schema: str):
        super().__init__(schema)

    def connect(self):
        self.connection = sqlite3.connect(database=self.schema)

    def get_cursor(self):
        if self.connection:
            self.cursor = self.connection.cursor()
        else:
            raise RuntimeError("No active sqlite3 connection!")

    def execute_script(self, script: str):
        if self.cursor:
            try:
                self.cursor.executescript(script)
                self.connection.commit()
            except sqlite3.OperationalError as e:
                print(e)
        else:
            raise RuntimeError("No active sqlite3 cursor!")

    def execute_statement(self, statement, parameters=(), fetch_one=False):
        if self.cursor:
            try:
                result = self.cursor.execute(statement, parameters)
                if not statement.startswith('SELECT'):
                    self.connection.commit()
                return result.fetchall() if not fetch_one else result.fetchone()
            except sqlite3.OperationalError as e:
                print(e)
        raise RuntimeError("No active sqlite3 cursor!")

    def close(self):
        self.close_cursor()
        self.close_connection()

    def close_cursor(self):
        if self.cursor:
            self.cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()


class TestDbClient:
    schema: str
    db_client: BaseDbClient
    SELECT_ALL_FROM_COMPANY = "SELECT * FROM COMPANY;"
    SELECT_COMPANY_BY_NAME = "SELECT * FROM COMPANY WHERE NAME=?"
    INSERT_COMPANY = "INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) VALUES(?, ?, ?, ?, ?)"

    def __init__(self, schema: str, db_client: BaseDbClient):
        self.schema = schema
        self.db_client = db_client

    def initialize(self, script_path: str):
        self.db_client.execute_script(utils.read_from_file(script_path))

    def get_companies(self):
        return self.db_client.execute_statement(self.SELECT_ALL_FROM_COMPANY, fetch_one=False)

    def get_company_by_name(self, name):
        return self.db_client.execute_statement(
            statement=self.SELECT_COMPANY_BY_NAME,
            parameters=(name,),
            fetch_one=True
        )

    def add_company(self, company):
        return self.db_client.execute_statement(
            statement=self.INSERT_COMPANY,
            parameters=company,
            fetch_one=True
        )
