from main_app import app
from flask import render_template

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/')
def login():
	return render_template('profile.html')

