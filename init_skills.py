from app import get_db_connection

def initialize_skills():
    skills = [
        ('Python', 3),
        ('Flask', 3),
        ('PostgreSQL', 3),
        ('JavaScript', 2),
        ('CSS', 4),
        ('Git', 4),
        ('HTML', 4),
        ('SQL', 4),
        ('C', 3),
        ('Figma', 3),
        ('Canva', 3),
        ('AutoDesk Fusion 360', 2),
        ('Adobe Illustrator', 2),
        ('Adobe Photoshop', 3),
        ('Adobe XD', 3),
        ('Arduino', 2),
        ('Access', 3),
        ('Excel', 4)
    ]

    conn = get_db_connection()
    cur = conn.cursor()

    # Insert initial skill ratings
    for tech, proficiency in skills:
        cur.execute("""
            INSERT INTO tech_stack (technology, proficiency)
            VALUES (%s,%s)
            ON CONFLICT (technology) DO UPDATE 
            SET proficiency = EXCLUDED.proficiency;
        """, [tech.lower(), vote_value])
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    initialize_skills()