from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root75@localhost/user_auth'
db = SQLAlchemy(app)

# Load course data
courses_df = pd.read_csv('cleaned_courses_data.csv')


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# Feedback model
class Feedback(db.Model):
    __tablename__ = 'Feedback'  # Ensure the correct table name case
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Feedback {self.id}>'


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/search_courses')
def search_courses():
    query = request.args.get('query', '')
    if query:
        suggestions = courses_df[courses_df['course_title'].str.contains(query, case=False, na=False)]
        suggestions = suggestions[['course_title']].drop_duplicates().head(10)
    else:
        suggestions = pd.DataFrame(columns=['course_title'])

    return jsonify({'suggestions': suggestions.to_dict(orient='records')})


@app.route('/recommend')
def recommend():
    course_title = request.args.get('course_title', '')
    difficulty = request.args.get('difficulty', 'All')

    filtered_courses = courses_df[courses_df['course_title'].str.contains(course_title, case=False, na=False)]

    if difficulty != 'All':
        filtered_courses = filtered_courses[filtered_courses['course_difficulty'] == difficulty]

    recommendations = filtered_courses.to_dict(orient='records')

    return jsonify({'recommendations': recommendations})


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists. Please choose a different username."

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid username or password. Please try again."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        category = request.form['category']
        feedback_text = request.form['feedback']
        rating = request.form['rating']

        # Create a new feedback entry
        new_feedback = Feedback(name=name, email=email, category=category, feedback=feedback_text, rating=rating)
        db.session.add(new_feedback)
        db.session.commit()

        # Redirect to home page after feedback submission
        return redirect(url_for('index'))

    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
