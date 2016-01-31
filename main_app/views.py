from main_app import app
from flask import render_template

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/')
<<<<<<< HEAD
def login():
	return render_template('login.html')
=======
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/courses')
def courses():
	return render_template('courses.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')
>>>>>>> d4ad797aed0447609c2ad550291634f6cc444442

@app.route('/forgot')
def forgot():
	return render_template('forgot.html')

@app.route('/login')
def login():
	return render_template('login.html')
