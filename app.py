import sys
import sqlite3
import os
from flask import Flask, render_template, request
from datetime import datetime
import psycopg
from urllib.parse import urlparse

app = Flask(__name__)

def get_db_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    conn = psycopg.connect(DATABASE_URL)
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

    cur.execute("DROP TABLE IF EXISTS tech_stack")
    cur.execute('''
        CREATE TABLE tech_stack (
            id SERIAL PRIMARY KEY,
            technology_key VARCHAR(255) UNIQUE,
            display_name VARCHAR(255),
            proficiency INT CHECK(proficiency >=1 AND proficiency <=5)
        )
    ''')

    #Seeding
    initial_skills = [ ('python', 'Python', 3),
                          ('flask', 'Flask', 3),
                          ('postgresql', 'PostgreSQL', 3),
                          ('javascript', 'JavaScript', 2),
                          ('css', 'CSS', 4),
                          ('git', 'Git', 4),
                          ('html', 'HTML', 4),
                          ('sql', 'SQL', 4),
                          ('c', 'C', 3),
                          ('figma', 'Figma', 3),
                          ('canva', 'Canva', 3),
                          ('autodesk fusion 360', 'Autodesk Fusion 360', 2),
                          ('adobe illustrator', 'Adobe Illustrator', 2),
                          ('adobe photoshop', 'Adobe Photoshop', 3),
                          ('adobe xd', 'Adobe XD', 3),
                          ('arduino', 'Arduino', 2),
                          ('access', 'Access', 3),
                          ('excel','Excel',4)
                        ]
    for tech_key, display_name, proficiency in initial_skills:
        cur.execute("""
            INSERT INTO tech_stack (technology_key, display_name, proficiency)
            VALUES (%s,%s,%s)
            ON CONFLICT (technology_key) DO NOTHING 
        """, [tech_key, display_name, proficiency])    

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
    return render_template('index.html', visitor_count=count, frontend_skills=get_skill_levels())

@app.route('/skills')
def skills():
    count = log_visit('skills')
    return render_template('skills.html', 
                         visitor_count=count,
                         frontend_skills=get_skill_levels())

@app.route('/rate-skill', methods=['POST'])
def rate_skill():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get votes from form
        tech = request.form.get('tech', '').strip()
        vote_value = int(request.form.get('vote', 0))

        if not tech or vote_value < 1 or vote_value > 5:
            return {'status': 'error', 'message': 'Invalid input'}

        tech_key = tech.lower() #lower for conflict
        display_name = tech #Proper cap
        
        # Store vote
        cur.execute("""
            INSERT INTO tech_stack(technology_key, display_name, proficiency)
            VALUES (%s,%s,%s)
            ON CONFLICT(technology_key) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    proficiency = EXCLUDED.proficiency
            RETURNING *
        """, [tech.key, display_name, vote_value])
        
        conn.commit()
    except Exception as e:
        print(f"Error saving vote {e}")
        return {'status': 'error', 'message': str(e)}  
    finally:
        if 'conn' in locals():
            conn.close()

    return {'status': 'success'}
 
def get_skill_levels():
     try:
         conn = get_db_connection()
         cur = conn.cursor()
         
         # Average votes per technology
         cur.execute("""
             SELECT display_name AS tech,
                     ROUND(AVG(proficiency)):: INT AS level 
             FROM tech_stack 
             GROUP BY display_name
             ORDER BY display_name
         """)
         
         result = {row: row[1] for row in cur.fetchall()}
         cur.close()
         conn.close()
         return result
          
     except Exception as e:
          print(f"Error getting levels {e}")
          return {}

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