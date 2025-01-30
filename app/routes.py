from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Category, Question, Choice
from app.forms import LoginForm, SignupForm, QuestionForm, CategoryForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin' if current_user.is_admin else 'dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin' if user.is_admin else 'dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose a different one.')
            return redirect(url_for('signup'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different one.')
            return redirect(url_for('signup'))
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    categories = Category.query.all()
    return render_template('dashboard.html', categories=categories)

@app.route('/quiz/<int:category_id>', methods=['GET', 'POST'])
@login_required
def quiz(category_id):
    category = Category.query.get_or_404(category_id)
    questions = db.session.query(Question).filter(Question.category_id == category_id).all()

    for question in questions:
        question.choices = Choice.query.filter_by(question_id=question.id).all()

    score = None  # Default value, updated after submission

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer = request.form.get(f"question_{question.id}")
            if selected_answer and selected_answer == question.answer:
                score += 10  # 10 points for correct answer

        return render_template('quiz.html', category=category, questions=questions, score=score)

    return render_template('quiz.html', category=category, questions=questions, score=None)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))
    
    category_form = CategoryForm()
    question_form = QuestionForm()
    
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "category" and category_form.validate_on_submit():
            category = Category(name=category_form.name.data)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully', 'success')
            return redirect(url_for('admin'))

        elif form_type == "question" and question_form.validate_on_submit():
            question = Question(
                text=question_form.text.data,
                answer=question_form.answer.data,
                category_id=question_form.category.data
            )
            db.session.add(question)
            db.session.commit()

            # Add choices for the question
            choices = [
                Choice(text=question_form.choice1.data, question_id=question.id),
                Choice(text=question_form.choice2.data, question_id=question.id),
                Choice(text=question_form.choice3.data, question_id=question.id),
                Choice(text=question_form.choice4.data, question_id=question.id)
            ]
            db.session.bulk_save_objects(choices)
            db.session.commit()

            flash('Question and choices added successfully', 'success')
            return redirect(url_for('admin'))

    return render_template('admin.html', category_form=category_form, question_form=question_form)
