from flask import Flask, render_template, redirect, request, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
#from flask_bcrypt import Bcrypt  #for hashing passwrd
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager, current_user

# =====INITIALISATION========
app = Flask(__name__)
app.secret_key = "this is for testing"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):
    return Login_test.query.get(int(user_id))


# =====Forms=======
class RegisterForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min=3, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators = [InputRequired(), Length(min=3, max=20)], render_kw={'placeholder':'Password'})
    submit = SubmitField("Register User")

class LoginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min=3, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators = [InputRequired(), Length(min=3, max=20)], render_kw={'placeholder':'Password'})
    submit = SubmitField("Login")

# =====MODELS======

class CRUD_test(db.Model):

    __table__name = "crud_test"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    mail = db.Column(db.String(30))

    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

    def __repr__(self):
        return str({
            "name": self.name,
            "mail": self.mail,
            "id": self.id
        })

class Login_test(db.Model, UserMixin):

    __table__name = "login_test"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return str({
            "username": self.username,
            "password": self.password,
            "id": self.id
        })

#=====ROUTES=======

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    print('in index')
    op = CRUD_test.query.all()
    users = Login_test.query.all()
    return render_template('index.html', data = op, users = users)

@app.route('/insert', methods=['GET', 'POST'])
def insertion():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        
        data = CRUD_test(name, mail)
        db.session.add(data)
        db.session.commit()

        print("inserted successfully")

        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def deletion(id):
    if request.method == 'GET':
        data = CRUD_test.query.get(id)
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/update/<int:id>', methods = ['GET','POST'])
def updation(id):
    if request.method == "GET":
        data = CRUD_test.query.get(id)
        return render_template('update_form.html', data=data)
    else:
        data = CRUD_test.query.get(id)
        data.name = request.form['name']
        data.mail = request.form['mail']
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        data = Login_test(username, password)
        db.session.add(data)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        data = Login_test.query.filter_by(username=form.username.data).first()
        if data and form.password.data == data.password:
            login_user(data)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)