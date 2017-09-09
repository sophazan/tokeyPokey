import os
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

class Users_Game(db.Model):
    __tablename__ = "users_game"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)

    def __init__(self, user_id, game_id):
        self.user_id = user_id
        self.game_id = game_id

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    rand_num = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(120))

    def __init__(self, rand_num, status):
        self.rand_num = rand_num
        self.status = status

class Game_Question(db.Model):
    __tablename__ = "game_question"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)

    def __init__(self, game_id, question_id):
        self.game_id = game_id
        self.question_id = question_id

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question_str = db.Column(db.String, unique=True)

    def __init__(self, question_str):
        self.question_str = question_str

def Result_Table(db.Model):
    __tablename__ = "result_table"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    question_id = id.Column(db.Integer)
    answer = db.Column(db.Boolean(120))
    guess = db.Column(db.Integer)
    guess_diff = db.Column(db.Integer)

    def __init__(self, game_id, user_id, question_id, answer, guess, guess_diff):
        self.game_id = game_id
        self.user_id = user_id        
        self.question_id = question_id
        self.answer = answer        
        self.guess = guess
        self.guess_diff = guess_diff

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()