import os
import psycopg

def reset_database():
    # Get the database URL from environment
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set.")
        return

    # Fix postgres:// if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    try:
        print(f"Connecting to database...")
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Drop the problematic table
        print("Dropping table 'tech_stack'...")
        cur.execute("DROP TABLE IF EXISTS tech_stack;")
        
        conn.commit()
        cur.close()
        conn.close()
        print("Table dropped successfully. Now run 'python app.py' to recreate it.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reset_database()