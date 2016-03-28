from flask import Flask, request, session, g
from flask import render_template, redirect, make_response, url_for, send_from_directory
import json, datetime
import psycopg2
from sqlalchemy import create_engine
from werkzeug import secure_filename
import os.path

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
        cursor = conn.execute("\
                              SELECT a.dept, c.prof, c.cid, c.name \
                              FROM course AS c \
                              JOIN affiliate AS a ON a.prof=c.prof \
                              JOIN subscribes AS s ON c.cid=s.course AND c.prof=s.course_prof \
                              WHERE s.usr = %s; \
                              ", session['email'])
        # put user subscribed courses into a row
        url = []; name = []; to_delete = []
        for row in cursor:
            course_id = '/delete/'+'/'.join(map(str, row[1:3]))
            if course_id not in to_delete:
                url.append('/courses/'+'/'.join(map(str, row[:3]))); name.append(row[3])
                to_delete.append(course_id)
        all_courses = conn.execute("\
                                   SELECT p.name, c.name, c.prof, c.cid \
                                   FROM course AS c, professor AS p \
                                   WHERE c.prof = p.id; \
                                   ")
        all_courses_lst = []
        for row in all_courses:
            all_courses_lst.append(row)
        return render_template('index.html', url=url, name=name,
                               user=session['email'], to_delete=to_delete,
                               all_courses_lst=all_courses_lst)
    else:
        return redirect(url_for('login'))

@application.route('/delete/<pid>/<cid>')
def delete_course(pid, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        conn.execute("\
                     DELETE FROM subscribes AS s \
                     WHERE s.course=%s AND s.course_prof=%s; \
                     ", str(cid), str(pid))
        conn.execute("\
                     DELETE FROM course_subscribes_usr AS s \
                     WHERE s.cid=%s AND s.prof=%s; \
                     ", str(cid), str(pid))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@application.route('/add/<pid>/<cid>')
def add_course(pid, cid):
    if 'email' in session:
        try:
            conn = getattr(g, 'conn', None)
            conn.execute("\
                         INSERT INTO subscribes (usr, course, course_prof) \
                         VALUES (%s, %s, %s); \
                         ", session['email'], int(cid), int(pid))
            conn.execute("\
                         INSERT INTO course_subscribes_usr (usr, cid, prof) \
                         VALUES (%s, %s, %s); \
                         ", session['email'], int(cid), int(pid))
            return redirect(url_for('index'))
        except: # course already in user's subscribed list
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@application.route('/courses')
def nav_dept():
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute("\
                              SELECT * \
                              FROM department AS d \
                              ORDER BY name; \
                              ")
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
        cursor = conn.execute("\
                              SELECT p.id, p.name \
                              FROM professor AS p \
                              JOIN affiliate AS a ON p.id=a.prof \
                              JOIN department AS d on d.id=a.dept \
                              WHERE d.id=%s; \
                              ", int(did))
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
        cursor = conn.execute("\
                              SELECT c.cid, c.name \
                              FROM course AS c \
                              WHERE c.prof=%s; \
                              ", int(pid))
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
        cursor = conn.execute("\
                              SELECT * \
                              FROM course AS c \
                              JOIN professor AS p ON c.prof = p.id \
                              WHERE c.prof=%s AND c.cid=%s; \
                              ", int(pid), int(cid))
        for row in cursor:
            course_name = row[2]
            prof_name = row[7]
            workload = row[3]
            rating = row[4]
        reviews = list(conn.execute("\
                                    SELECT * \
                                    FROM review AS r \
                                    WHERE r.prof=%s AND r.cid=%s; \
                                    ", int(pid), int(cid)))
        documents = list(conn.execute("\
                                    SELECT * \
                                    FROM document AS d \
                                    WHERE d.prof=%s AND d.cid=%s; \
                                    ", int(pid), int(cid)))
        return render_template('course.html', user=session['email'],
                                course_name=course_name,
                                prof_name=prof_name,
                                reviews=reviews,
                                documents=documents,
                                did=did,
                                pid=pid,
                                cid=cid,
                                rating=rating,
                                workload=workload)
    else:
        return redirect(url_for('login'))

@application.route('/review/<did>/<pid>/<cid>', methods=['POST'])
def modify_review(did, pid, cid):
    if 'email' in session:
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d")
        conn = getattr(g, 'conn', None)
        # Insert data for review
        cursor = conn.execute("\
                              SELECT * \
                              FROM course_subscribes_usr AS c \
                              WHERE c.usr=%s AND c.cid=%s AND c.prof=%s; \
                              ", session['email'], int(cid), int(pid))
        for row in cursor:
            try:
                conn.execute("\
                             INSERT INTO review (usr, cid, prof, content, create_date, update_date) \
                             VALUES (%s, %s, %s, %s, %s, %s); \
                             ", session['email'], int(cid), int(pid), request.form['comment'], now, now)
            except Exception:
                conn.execute("\
                             UPDATE review \
                             SET content=%s, update_date=%s \
                             WHERE usr=%s AND cid=%s AND prof=%s; \
                             ", request.form['comment'], now, session['email'], int(cid), int(pid))
        return redirect('/courses/' + did + '/' + pid + '/' + cid)
    else:
        return redirect(url_for('login'))

@application.route('/document/<did>/<pid>/<cid>', methods=['GET', 'POST'])
def documents(did, pid, cid):
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        if request.method == 'GET':
            cursor = conn.execute("\
                                  SELECT file_location \
                                  FROM document \
                                  WHERE did=%s AND usr=%s AND cid=%s AND prof=%s; \
                                  ", int(request.args['doc']), session['email'], int(cid), int(pid))
            for row in cursor:
                return send_from_directory('data', row[0], as_attachment=True)
        else:
            to_upload = request.files['file']
            if to_upload:
                filename = secure_filename(to_upload.filename)
                to_upload.save(os.path.join('data', filename))
                conn.execute("\
                             INSERT INTO document (usr, cid, prof, name, file_location, create_date) \
                             VALUES (%s, %s, %s, %s, %s, %s)",
                            session['email'],
                            int(cid),
                            int(pid),
                            request.form['name'],
                            filename,
                            datetime.datetime.now().strftime("%Y-%m-%d"))
            return redirect('/'.join(['/courses', did, pid, cid]))
    else:
        return redirect(url_for('login'))

@application.route('/courses/rate/<did>/<pid>/<cid>', methods=['POST'])
def rate_course(did, pid, cid):
    ''' Function to rate a particular course.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        cursor = conn.execute("\
                              SELECT * \
                              FROM course_subscribes_usr AS c \
                              WHERE usr=%s AND cid=%s AND prof=%s; \
                              ", session['email'], int(cid), int(pid))
        for item in cursor:
            # first get current rating, workload, and vote count
            course = conn.execute("\
                                  SELECT c.name, c.workload, c.star, c.vote_count \
                                  FROM course AS c \
                                  WHERE c.prof=%s AND c.cid=%s; \
                                  ", int(pid), int(cid))
            for row in course:
                votes = row
            course_name = votes[0]
            # the first vote!
            if votes[3] == None:
                cursor = conn.execute("\
                                      UPDATE course AS c \
                                      SET workload = %s, \
                                      star = %s, \
                                      vote_count = %s \
                                      WHERE prof = %s AND cid = %s; \
                                      ", float(request.form['workload']),
                                         float(request.form['stars']), 1,
                                         int(pid), int(cid))
                return redirect('/courses/' + did + '/' + pid + '/' + cid)
            # not the first vote, so take this vote with weighted moving average
            else:
                curr_stars = float(votes[2])
                curr_workload = float(votes[1])
                curr_votes = votes[3]
                # new weighted moving average of workload
                new_workload = (((curr_workload * curr_votes) + float(request.form['workload'])) / (curr_votes + 1))
                # new weighted moving average of stars
                new_stars = (((curr_stars * curr_votes) + float(request.form['stars'])) / (curr_votes + 1))
                # insert values and iterate vote count
                cursor = conn.execute("\
                                      UPDATE course AS c \
                                      SET workload = %s, star = %s, vote_count = %s \
                                      WHERE prof = %s AND cid = %s; \
                                      ", new_workload, new_stars,
                                         curr_votes + 1,
                                         int(pid), int(cid))
        return redirect('/courses/' + did + '/' + pid + '/' + cid)
    else:
        return redirect(url_for('login'))

@application.route('/review/rate/<did>/<pid>/<cid>/<rid>', methods=['POST'])
def rate_review(did, pid, cid, rid):
    ''' Function to rate a particular review for a course.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        # first get current review rating and vote count
        reviews = conn.execute("\
                              SELECT r.star, r.vote_count \
                              FROM review AS r \
                              WHERE r.rid=%s; \
                              ", int(rid))
        for row in reviews:
            review = row
        # the first vote!
        if review[1] == None:
            cursor = conn.execute("\
                                  UPDATE review \
                                  SET star = %s, \
                                  vote_count = %s \
                                  WHERE rid = %s; \
                                  ", float(request.form['stars']),
                                     1, int(rid))
            return redirect('/courses/' + did + '/' + pid + '/' + cid)
        # not the first vote, so take this vote with weighted moving average
        else:
            curr_stars = float(review[0])
            curr_votes = review[1]
            # new weighted moving average of stars
            new_stars = (((curr_stars * curr_votes) + float(request.form['stars'])) / (curr_votes + 1))
            # insert values and iterate vote count
            cursor = conn.execute("\
                                  UPDATE review \
                                  SET star = %s, \
                                  vote_count = %s \
                                  WHERE rid = %s; \
                                  ", new_stars, curr_votes + 1,
                                     int(rid))
        return redirect('/courses/' + did + '/' + pid + '/' + cid)
    else:
        return redirect(url_for('login'))


@application.route('/report/review/<did>/<pid>/<cid>/<rid>', methods=['GET'])
def report_review(did, pid, cid, rid):
    ''' Function to report a review for a course.
    '''
    if 'email' in session:
        if request.method == 'GET':
            conn = getattr(g, 'conn', None)
            # first get current review rating and vote count
            reviews = conn.execute("\
                                  SELECT r.report_count \
                                  FROM review AS r \
                                  WHERE r.rid=%s; \
                                  ", int(rid))
            for row in reviews:
                review = row
                print "here"
                print review
            # the first report!
            if review[0] == None:
                cursor = conn.execute("\
                                      UPDATE review \
                                      SET report_count = %s \
                                      WHERE rid = %s; \
                                      ", 1, int(rid))
                return redirect('/courses/' + did + '/' + pid + '/' + cid)
            # not the report
            else:
                print "here2"
                cursor = conn.execute("\
                                      UPDATE review \
                                      SET report_count = %s \
                                      WHERE rid = %s; \
                                      ", int(review[0]) + 1, int(rid))
            return redirect('/courses/' + did + '/' + pid + '/' + cid)
        else:
            return redirect('/courses/' + did + '/' + pid + '/' + cid)
    else:
        return redirect(url_for('login'))

@application.route('/document/rate/<did>/<pid>/<cid>/<doc>', methods=['POST'])
def rate_doc(did, pid, cid, doc):
    ''' Function to rate a particular review for a course.
    '''
    if 'email' in session:
        conn = getattr(g, 'conn', None)
        # first get current review rating and vote count
        documents = conn.execute("\
                              SELECT d.star, d.vote_count \
                              FROM document AS d \
                              WHERE d.did=%s; \
                              ", int(doc))
        for row in documents:
            # the first vote!
            if row[1] == None:
                cursor = conn.execute("\
                                      UPDATE document \
                                      SET star = %s, \
                                      vote_count = %s \
                                      WHERE did = %s; \
                                      ", float(request.form['stars']),
                                         1, int(doc))
                return redirect('/courses/' + did + '/' + pid + '/' + cid)
            # not the first vote, so take this vote with weighted moving average
            else:
                curr_stars = float(row[0])
                curr_votes = row[1]
                # new weighted moving average of stars
                new_stars = (((curr_stars * curr_votes) + float(request.form['stars'])) / (curr_votes + 1))
                # insert values and iterate vote count
                cursor = conn.execute("\
                                      UPDATE document \
                                      SET star = %s, \
                                      vote_count = %s \
                                      WHERE did = %s; \
                                      ", new_stars, curr_votes + 1,
                                         int(rid))
        return redirect('/courses/' + did + '/' + pid + '/' + cid)
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
        cursor = conn.execute("\
                              SELECT u.passwd \
                              FROM usr AS u \
                              WHERE u.e_mail=%s; \
                              ", request.form['email'])
        for row in cursor:
            if row['passwd'] == request.form['passwd_origin']: break
        else:
            return render_template('profile.html', email = session['email'], is_valid='no', user=session['email'])
        if request.form['passwd_change'] != request.form['passwd_validate']:
            return render_template('profile.html', email = session['email'], is_valid='no', user=session['email'])
        else:
            conn.execute("\
                         UPDATE usr \
                         SET passwd=%s \
                         WHERE e_mail=%s \
                         ", request.form['passwd_change'], request.form['email'])
            return render_template('profile.html', email=session['email'], is_valid='yes', user=session['email'])

@application.route('/register', methods=['POST'])
def register():
    conn = getattr(g, 'conn', None)
    try:
        conn.execute("\
                     INSERT INTO usr (name, passwd, e_mail) \
                     VALUES (%s, %s, %s); \
                     ", request.form['name'], request.form['passwd'], request.form['email'])
        session['email'] = request.form['email']
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for('login'))

@application.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        conn = getattr(g, 'conn', None)
        cursor = conn.execute("\
                              SELECT * \
                              FROM usr \
                              WHERE e_mail=%s AND passwd=%s; \
                              ", request.form['email'], request.form['passwd'])
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
