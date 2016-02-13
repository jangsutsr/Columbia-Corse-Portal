from main_app import app
from flask import render_template, request, redirect, make_response
import json

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/')
@app.route('/index')
def index():
    if 'uni' in request.cookies and request.cookies['uni'] == 'hehehehe':
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/courses')
def courses():
	return render_template('courses.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/register', methods=['POST'])
def ajax_register():
    for name in request.form:
        print(name+', '+request.form[name])
    return json.dumps({'Stat': 'OK'})

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        is_valid = True
        for name in request.form:
            if request.form[name] == '':
                is_valid = False; break
        if is_valid:
            data = json.dumps({'redirect': True, 'url': '/index'})
            response = make_response(data)
            response.set_cookie('uni', value=request.form['uni'])
            return response
        else:
            return json.dumps({'redirect': False})
    else:
        return render_template('login.html')
