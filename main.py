import git
import os
from dotenv import load_dotenv

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, MilkForm
from flask_behind_proxy import FlaskBehindProxy

load_dotenv()
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
  return render_template('landing.html', subtitle='Welcome!', text='This is the home page.')

# @app.route("/database")
# def second_page():
#   return render_template('second_page.html', subtitle='Database', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template('register.html', title='Register', form=form)

@app.route("/submit-a-milk", methods=['GET', 'POST'])
def submit_milk():
    form = MilkForm()
    if form.validate_on_submit():
        flash(f'Your feelings about {form.milk_type.data} have been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('submit_milk.html', title='Got Any Milk?', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/ysabelleablir/Flask-App')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")