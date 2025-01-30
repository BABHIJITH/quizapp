from app import db
from app.models import Category, Question, Choice

# Delete all records from the tables
db.session.query(Choice).delete()
db.session.query(Question).delete()
db.session.query(Category).delete()

# Commit the changes
db.session.commit()

print("Database cleared successfully!")
