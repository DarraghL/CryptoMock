from app import create_app, db
import logging

logger = logging.getLogger(__name__)

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            logger.info("Dropped all tables successfully")
            
            # Create all tables
            db.create_all()
            logger.info("Created all tables with new schema")
            
            print("Database reset completed successfully!")
            
        except Exception as e:
            logger.error(f"Error resetting database: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    reset_database()