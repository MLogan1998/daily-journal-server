import sqlite3
import json

from models.entry import Entry
from models.mood import Mood

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.moodId
        """)

        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
          entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

          mood = Mood(row['moodId'], row['mood_label'])
        
          entry.mood = mood.__dict__
          
          entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.moodId
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['moodId'])

        mood = Mood(data['moodId'], data['mood_label'])

        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, ( id, ))


def get_entry_by_keyword(keyword):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM Entries e
        WHERE e.entry LIKE  ?
        """, ( '%'+keyword+'%', ))

        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
          entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])
          entries.append(entry.__dict__)

    return json.dumps(entries)
