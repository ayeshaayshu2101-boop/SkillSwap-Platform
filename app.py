from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillswap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

# Skill Table
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teach_skill = db.Column(db.String(100))
    learn_skill = db.Column(db.String(100))
    experience = db.Column(db.String(100))

# Session Table
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))

# Review Table
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(20))
    review = db.Column(db.String(500))

with app.app_context():
    db.create_all()

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password']
        )

        db.session.add(user)
        db.session.commit()

        return "Registration Successful!"

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return render_template('dashboard.html')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Add Skill
@app.route('/addskill', methods=['GET', 'POST'])
def addskill():

    if request.method == 'POST':

        skill = Skill(
            teach_skill=request.form['teach_skill'],
            learn_skill=request.form['learn_skill'],
            experience=request.form['experience']
        )

        db.session.add(skill)
        db.session.commit()

        return "Skill Saved Successfully!"

    return render_template('add_skill.html')

# Search Skills
@app.route('/search', methods=['GET', 'POST'])
def search():

    results = []

    if request.method == 'POST':

        skill_name = request.form['skill']

        results = Skill.query.filter(
            Skill.teach_skill.contains(skill_name)
        ).all()

    return render_template(
        'search.html',
        results=results
    )

# Profile
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Session Booking
@app.route('/session', methods=['GET', 'POST'])
def session():

    if request.method == 'POST':

        new_session = Session(
            date=request.form['date'],
            time=request.form['time']
        )

        db.session.add(new_session)
        db.session.commit()

        return "Session Booked Successfully!"

    return render_template('session.html')

# Reviews
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'POST':

        new_review = Review(
            rating=request.form['rating'],
            review=request.form['review']
        )

        db.session.add(new_review)
        db.session.commit()

        return "Review Submitted Successfully!"

    return render_template('reviews.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)