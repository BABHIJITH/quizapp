from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import Category

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

class QuestionForm(FlaskForm):
    text = TextAreaField('Question', validators=[DataRequired()])
    choice1 = StringField('Choice 1', validators=[DataRequired()])
    choice2 = StringField('Choice 2', validators=[DataRequired()])
    choice3 = StringField('Choice 3', validators=[DataRequired()])
    choice4 = StringField('Choice 4', validators=[DataRequired()])
    answer = RadioField('Correct Answer', choices=[
        ('choice1', 'Choice 1'), 
        ('choice2', 'Choice 2'), 
        ('choice3', 'Choice 3'), 
        ('choice4', 'Choice 4')
    ], validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Add Question')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
