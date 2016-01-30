from main_app import app
from flask import render_template

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/courses')
def courses():
	return render_template('courses.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/forgot')
def forgot():
	return render_template('forgot.html')

@app.route('/login')
def login():
	return render_template('login.html')
