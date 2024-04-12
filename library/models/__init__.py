import sqlite3

CONN = sqlite3.connect('ticket_tracker.db')
CURSOR = CONN.cursor()