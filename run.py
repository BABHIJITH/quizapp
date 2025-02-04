from app import app, db
from app.models import User, Category, Question, Choice  

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Category': Category, 'Question': Question, 'Choice': Choice}  

if __name__ == '__main__':
    app.run(debug=True)
