from flask import Flask, request, session, g
from flask import render_template, redirect, make_response, url_for
import json
import psycopg2
from sqlalchemy import create_engine

application = Flask(__name__)
application.jinja_env.trim_blocks = True
application.jinja_env.lstrip_blocks = True
application.secret_key = "hehefuck"

db = create_engine('postgresql://', creator=lambda _:psycopg2.connect(database='',
                                                                      user='st2957',
                                                                      password='MWRSCW',
                                                                      host='w4111db.eastus.cloudapp.azure.com'))

@application.before_request
def conn_db():
    ''' Establish a new db connection before view functions.
    '''
    g.conn = db.connect()

@application.teardown_request
def disconn_db(exception):
    ''' Terminate the db connection after response is sent.
    '''
    conn = getattr(g, 'conn', None)
    if conn is not None:
        conn.close()

@application.route('/')
def index():
    ''' View function for base url.
    Here the user's subscribed courses would be queried and rendered.
    Also, the department info are selected and rendered which would be used
    as navigation baselines.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT c.name AS n, c.prof AS p, c.cid AS c
                              FROM course AS c
                              JOIN subscribes AS s
                              ON c.cid=s.course AND c.prof=s.course_prof
                              WHERE s.usr = '{}';
                              '''.format(session['email']))
        for row in cursor:
            print(row['n'], row['p'], row['c'])
        cursor = conn.execute('''
                              SELECT *
                              FROM department;
                              ''')
        for row in cursor:
            print(row.items())
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@application.route('/navigate')
def navigate():
    ''' View function for navigations.
    Here the navigation info is represented by REST querys. query
    'dept' prompts for navigating professors affiliating particular
    department; 'prof' alone prompts for navigating courses taught
    by particular professor; 'prof' along with 'course' redirects
    to corresponding course page.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        if 'dept' in request.args:
            index = request.args['dept']
            cursor = conn.execute('''
                                  SELECT p.id AS id, p.name AS name
                                  FROM professor AS p
                                  JOIN affiliate AS a ON a.prof=p.id
                                  JOIN department AS d ON d.id=a.dept
                                  WHERE d.id={};
                                  '''.format(int(index)))
            for row in cursor:
                print(row.items())
            return 'profs'
        if 'prof' in request.args:
            if 'course' in request.args:
                return redirect(url_for('/'.join(['/courses', request.args['prof'], request.args['course']])))
            else:
                index = request.args['prof']
                cursor = conn.execute('''
                                      SELECT c.cid AS id, c.name AS name
                                      FROM course AS c
                                      WHERE c.prof={};
                                      '''.format(int(index)))
                for row in cursor:
                    print(row.items())
                return 'courses'
    else:
        return redirect(url_for('login'))

@application.route('/courses/<prof>/<cid>')
def courses(prof, cid):
    ''' View function for a particular course.
    This view is supposed to give a general information of a course.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM course AS c
                              WHERE c.prof={} AND c.cid={};
                              '''.format(int(prof), int(cid)))
        for row in cursor:
            print(row.items())
        return render_template('courses.html')
    else:
        return redirect(url_for('login'))

@application.route('/reviews/<prof>/<cid>')
def reviews(prof, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM review AS r
                              WHERE r.prof={} AND r.cid={};
                              '''.format(int(prof), int(cid)))
        for row in cursor:
            print(row.items())
        return render_template('reviews.html')
    else:
        return redirect(url_for('login'))

@application.route('/documents/<prof>/<cid>')
def documents(prof, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM document AS d
                              WHERE d.prof={} AND d.cid={};
                              '''.format(int(prof), int(cid)))
        for row in cursor:
            print(row.items())
        return render_template('documents.html')
    else:
        return redirect(url_for('login'))

@application.route('/profile')
def profile():
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM course AS c
                              WHERE c.prof={} AND c.cid={};
                              '''.format(int(prof), int(cid)))
        for row in cursor:
            print(row.items())
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@application.route('/register', methods=['POST'])
def register():
    conn = getattr(g, 'conn', None)
    try:
        conn.execute('''
                     INSERT INTO usr (name, passwd, e_mail)
                     VALUES ('{}', '{}', '{}');
                     '''.format(request.form['name'], request.form['passwd'], request.form['email']))
        session['email'] = request.form['email']
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for('login'))

@application.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT e_mail, passwd
                              FROM usr
                              WHERE e_mail='{}' AND passwd='{}';
                              '''.format(request.form['email'], request.form['passwd']))
        for row in cursor:
            session['email'] = row['e_mail']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    else:
        return render_template('login.html')

@application.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
