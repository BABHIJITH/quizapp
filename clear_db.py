from app import app, db
from app.models import Category, Question, Choice

def clear_database():
    with app.app_context():
        db.session.query(Choice).delete()
        db.session.query(Question).delete()
        db.session.query(Category).delete()
        db.session.commit()

if __name__ == '__main__':
    clear_database()
    print("Database cleared successfully!")
