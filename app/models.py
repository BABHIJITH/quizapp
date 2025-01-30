from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    questions = db.relationship('Question', backref='category', lazy='dynamic')

    def __repr__(self):
        return f"<Category {self.name}>"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    answer = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Relationship to choices
    choices = db.relationship('Choice', backref='question', lazy='dynamic')

    def __repr__(self):
        return f"<Question {self.text[:50]}>"

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))  # Choice text
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))  # Foreign key to Question

    def __repr__(self):
        return f"<Choice {self.text[:50]}>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
