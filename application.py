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
        print 'close'

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
                              SELECT a.dept, c.prof, c.cid, c.name
                              FROM course AS c
                              JOIN affiliate AS a ON a.prof=c.prof
                              JOIN subscribes AS s ON c.cid=s.course AND c.prof=s.course_prof
                              WHERE s.usr = '{}';
                              '''.format(session['email']))
        # put user subscribed courses into a row
        url = []; name = []; to_delete = []
        for row in cursor:
            course_id = '/delete/'+'/'.join(map(str, row[1:3]))
            if course_id not in to_delete:
                url.append('/courses/'+'/'.join(map(str, row[:3]))); name.append(row[3])
                to_delete.append(course_id)
        return render_template('index.html', url=url, name=name, user=session['email'], to_delete=to_delete)
    else:
        return redirect(url_for('login'))

@application.route('/delete/<pid>/<cid>')
def delete_course(pid, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        conn.execute('''
                     DELETE FROM subscribes AS s
                     WHERE s.course={} AND s.course_prof={};
                     '''.format(str(cid), str(pid)))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@application.route('/courses')
def nav_dept():
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM department AS d
                              ORDER BY name;
                              ''')
        urls = []; names = []
        for row in cursor:
            urls.append('/courses/'+str(row[0])); names.append(row[1])
        return render_template('courses.html', url=urls, name=names, header='Departments', user=session['email'])
    else:
        return redirect(url_for('login'))

@application.route('/courses/<did>')
def nav_prof(did):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT p.id, p.name
                              FROM professor AS p
                              JOIN affiliate AS a ON p.id=a.prof
                              JOIN department AS d on d.id=a.dept
                              WHERE d.id={};
                              '''.format(int(did)))
        urls = []; names = []
        for row in cursor:
            urls.append('/courses/'+did+'/'+str(row[0])); names.append(row[1])
        return render_template('courses.html', url=urls, name=names, header='Professors', user=session['email'])
    else:
        return redirect(url_for('login'))

@application.route('/courses/<did>/<pid>')
def nav_course(did, pid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT c.cid, c.name
                              FROM course AS c
                              WHERE c.prof={};
                              '''.format(int(pid)))
        urls = []; names = []
        for row in cursor:
            urls.append('/courses/'+did+'/'+pid+'/'+str(row[0])); names.append(row[1])
        return render_template('courses.html', url=urls, name=names, header='Courses', user=session['email'])
    else:
        return redirect(url_for('login'))

@application.route('/courses/<did>/<pid>/<cid>')
def course_info(did, pid, cid):
    ''' View function for a particular course.
    This view is supposed to give a general information of a course.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute('''
                              SELECT *
                              FROM course AS c
                              JOIN professor AS p ON c.prof = p.id
                              WHERE c.prof={} AND c.cid={};
                              '''.format(int(pid), int(cid)))
        for row in cursor:
            course_name = row[2]
            prof_name = row[7]
        reviews = conn.execute('''
                              SELECT *
                              FROM review AS r
                              WHERE r.prof={} AND r.cid={};
                              '''.format(int(pid), int(cid)))
        reviews = list(reviews)
        return render_template('course.html', user=session['email'],
                                course_name=course_name, prof_name=prof_name,
                                reviews=reviews)
    else:
        return redirect(url_for('login'))

@application.route('/review/<rid>/<usr>/<cid>/<prof>', methods=['GET', 'POST'])
def reviews(prof, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        if request.method == 'GET':
            pass
        else:
            pass
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
        return render_template('documents.html', user=session['email'])
    else:
        return redirect(url_for('login'))

@application.route('/profile', methods=['POST', 'GET'])
def profile():
    conn = getattr(g, 'conn', None)
    if request.method == 'GET':
        if 'email' in session:
            return render_template('profile.html', email = session['email'], is_valid='yes', user=session['email'])
        else:
            return redirect(url_for('login'))
    else:
        cursor = conn.execute('''
                              SELECT u.passwd
                              FROM usr AS u
                              WHERE u.e_mail='{}';
                              '''.format(request.form['email']))
        for row in cursor:
            if row['passwd'] == request.form['passwd_origin']: break
        else:
            return render_template('profile.html', email = session['email'], is_valid='no', user=session['email'])
        if request.form['passwd_change'] != request.form['passwd_validate']:
            return render_template('profile.html', email = session['email'], is_valid='no', user=session['email'])
        else:
            conn.execute('''
                         UPDATE usr
                         SET passwd='{}'
                         WHERE e_mail='{}';
                         '''.format(request.form['passwd_change'], request.form['email']))
            return render_template('profile.html', email=session['email'], is_valid='yes', user=session['email'])

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
                              SELECT *
                              FROM usr
                              WHERE e_mail='{}' AND passwd='{}';
                              '''.format(request.form['email'], request.form['passwd']))
        for row in cursor:
            print row['e_mail']
            session['email'] = row['e_mail']
            session['name'] = row['name']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    else:
        return render_template('login.html')

@application.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
