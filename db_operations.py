import sqlite3

class DbOperation:

    """
    Klasa DbOperation zapewnia interfejs do operacji CRUD na bazie danych SQLite.
    
    Jest to klasa Singleton, co oznacza, że zawsze istnieje tylko jedna instancja tej klasy.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DbOperation, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Inicjalizuje obiekt DbOperation z pustą listą obserwatorów."""
        self._observers = []

    def connect_to_db(self):
        """
        Łączy się z bazą danych SQLite.

        :return: Połączenie do bazy danych
        """
        conn = sqlite3.connect("password_records.db")
        return conn

    def create_table(self, table_name="password_info"):
        """
        Tworzy tabelę w bazie danych, jeśli nie istnieje.

        :param table_name: Nazwa tabeli
        """
        conn = self.connect_to_db()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            username VARCHAR(200) DEFAULT NULL,
            password VARCHAR(50) DEFAULT NULL
        );
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name="password_info"):
        """
        Tworzy nowy rekord w tabeli.

        :param data: Słownik z danymi rekordu
        :param table_name: Nazwa tabeli
        """
        title = data['title']
        username = data['username']
        password = data['password']
        conn = self.connect_to_db()
        query = f'''
        INSERT INTO {table_name} ('title', 'username', 'password') VALUES ( ?, ?, ?)
        ;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (title, username, password))
            print("Saved the record", (title, username, password))
        self.notify_observers()

    def show_records(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query)
            return list_records
        
    def delete_table(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f"DROP TABLE IF EXISTS {table_name};"
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def update_record(self, data, table_name="password_info"):
        ID = data['ID']
        title = data['title']
        username = data['username']
        password = data['password']
        conn = self.connect_to_db()
        query = f'''
        UPDATE {table_name} SET title = ?, username = ?, password = ? 
        WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (title, username, password, ID))
        self.notify_observers()

    def delete_record(self, ID, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        DELETE FROM {table_name} WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ID,))
        self.notify_observers()

    def search_records(self, title, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name} WHERE title LIKE ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query, ('%'+title+'%',))
            return list_records

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()
