# backend/tests/test_db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.sql import text

def test_connection():
    try:
        # Create engine
        engine = create_engine('postgresql://daz:darragh1@localhost:5432/stocksim')
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Database connection successful!")
            
            # Test if we can create tables (optional)
            connection.execute(text('CREATE TABLE IF NOT EXISTS test_connection (id serial PRIMARY KEY)'))
            print("Table creation successful!")
            
            # Clean up test table
            connection.execute(text('DROP TABLE IF EXISTS test_connection'))
            
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_connection()