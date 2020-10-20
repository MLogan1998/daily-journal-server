import sqlite3
import json

from models.mood import Mood 

def get_all_moods():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          m.id,
          m.label
        FROM Moods m
        """)

        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:
          mood = Mood(row['id'], row['label'])
          moods.append(mood.__dict__)

    return json.dumps(moods)


def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          m.id,
          m.label
        FROM Moods m
        WHERE m.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        mood = Mood(data['id'], data['label'])

        return json.dumps(mood.__dict__)
