import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('game_records.db')
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                time_played INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def add_record(self, score, time_played):
        self.cursor.execute('''
            INSERT INTO records (score, time_played)
            VALUES (?, ?)
        ''', (score, time_played))
        self.conn.commit()
    
    def get_top_records(self, limit=10):
        self.cursor.execute('''
            SELECT score, time_played
            FROM records
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall() 