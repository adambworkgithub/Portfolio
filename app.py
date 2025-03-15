from flask import Flask, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Initialize the database
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

# Logs visits and retrieves visit counts
def log_visit(page):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("INSERT INTO visitors (timestamp, page) VALUES (?, ?)", (datetime.now(), page))
    conn.commit()
    c.execute("SELECT COUNT(*) FROM visitors WHERE page=?", (page,))
    count = c.fetchone()[0]
    conn.close()
    return count

# Routing for home page
@app.route('/')
def home():
    count = log_visit('home')
    return render_template('index.html', visitor_count=count)

# Routing for experience page
@app.route('/experience')
def experience():
    count = log_visit('experience')
    return render_template('experience.html', visitor_count=count)

# Routing for projects page
@app.route('/projects')
def projects():
    count = log_visit('projects')
    return render_template('projects.html', visitor_count=count)

# Routing for contact page
@app.route('/contact')
def contact():
    count = log_visit('contact')
    return render_template('contact.html', visitor_count=count)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)