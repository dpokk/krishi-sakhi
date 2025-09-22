import sqlite3
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path="KHETGPT/memory/agent_memory.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        # Ensure directory exists
        dir_path = os.path.dirname(self.db_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Table for storing farmer inputs and recommendations
        c.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                agent TEXT,
                user_input TEXT,
                agent_response TEXT
            )
        ''')

        # Table for storing crop recommendations and market trends
        c.execute('''
            CREATE TABLE IF NOT EXISTS crop_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                crop TEXT,
                predicted_price REAL,
                demand_forecast TEXT,
                recommended_by TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def log_interaction(self, agent, user_input, agent_response):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO interactions (timestamp, agent, user_input, agent_response)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), agent, user_input, agent_response))
        conn.commit()
        conn.close()

    def log_crop_suggestion(self, crop, predicted_price, demand_forecast, recommended_by):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO crop_suggestions (timestamp, crop, predicted_price, demand_forecast, recommended_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), crop, predicted_price, demand_forecast, recommended_by))
        conn.commit()
        conn.close()

    def fetch_all_interactions(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM interactions ORDER BY timestamp DESC')
        results = c.fetchall()
        conn.close()
        return results

    def fetch_all_crop_suggestions(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM crop_suggestions ORDER BY timestamp DESC')
        results = c.fetchall()
        conn.close()
        return results
