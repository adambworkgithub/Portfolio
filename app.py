import os
from flask import Flask, render_template
from datetime import datetime
import sqlite3  # Will need to replace with PostgreSQL for Heroku

app = Flask(__name__)

# For Heroku PostgreSQL (you'll need to set this up)
# DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///visitors.db')

def init_db():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            page TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_visit(page):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("INSERT INTO visitors (timestamp, page) VALUES (?, ?)", 
             (datetime.now(), page))
    conn.commit()
    c.execute("SELECT COUNT(*) FROM visitors WHERE page=?", (page,))
    count = c.fetchone()[0]
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
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production