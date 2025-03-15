import os
from flask import Flask, render_template
from datetime import datetime
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

def get_db_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            page TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def log_visit(page):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visitors (timestamp, page) VALUES (%s, %s)",
             (datetime.now(), page))
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visitors WHERE page=%s", (page,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

@app.route('/')
def home():
    count = log_visit('home')
    return render_template('index.html', visitor_count=count)

@app.route('/experience')
def experience():
    count = log_visit('experience')
    return render_template('experience.html', visitor_count=count)

@app.route('/projects')
def projects():
    count = log_visit('projects')
    return render_template('projects.html', visitor_count=count)

@app.route('/contact')
def contact():
    count = log_visit('contact')
    return render_template('contact.html', visitor_count=count)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)