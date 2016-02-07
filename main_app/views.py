from main_app import app
from flask import render_template, request
import json

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/<uni>/index')
def index(uni):
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

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/ajax/register', methods=['POST'])
def ajax_register():
    for name in request.form:
        print(name+', '+request.form[name])
    return json.dumps({'Stat': 'OK'})

@app.route('/ajax/login', methods=['POST'])
def ajax_login():
    is_valid = True
    for name in request.form:
        if request.form[name] == '':
            is_valid = False; break
    if is_valid:
        return json.dumps({'redirect': True, 'url': '/'+request.form['uni']+'/index'})
    else:
        return json.dumps({'redirect': False})
