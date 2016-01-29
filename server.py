from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

'''
Note server behaviors here are for front-end design only at present.
'''
@app.route('/')
def login():
	return render_template('login.html') 


if __name__ == '__main__':
	app.run(debug=True)