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

    
    for tech, proficiency in skills:
        tech_key = tech.lower()
        display_name = tech

        cur.execute("""
            INSERT INTO tech_stack (technology_key, display_name, proficiency)
            VALUES (%s,%s,%s)
            ON CONFLICT (technology_key) DO UPDATE 
            SET display_name = EXCLUDED.display_name,
                proficiency = EXCLUDED.proficiency;
        """, [tech_key, display_name, proficiency])
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    initialize_skills()