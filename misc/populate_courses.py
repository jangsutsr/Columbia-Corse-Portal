import requests
import psycopg2

'''
This script is meant for populating our database with real-world data. Here we use
REST api provided by CULPA to extract department, professor and course infomation.
The idea is firstly filling in departments according to the given dept_id array. Then
professor infomation are extracted based on searching result using dept_id. Finally
we populate course table w.r.t each professor.

Note there are situations where a professor affiliates more than one department and
a course is related to zero to many departments. Therefore we add two auxiliary
tables: affiliate and relate to represent these relations.
'''
dept_id = [7, 20, 57] # Department of CS, Physics and OR are chosen here
host_name = 'http://api.culpa.info'
department_search = '/departments/department_id/'
professor_search = '/professors/department_id/'
course_search = '/courses/professor_id/'

def insert_courses(prof, cursor):
    courses = requests.get(host_name + course_search + str(prof)).json()['courses']
    for course in courses:
        if course['number'] and course['name']:
            course_dept = course['department_ids']
            course_id = course['id']
            course_name = course['number'] + ' ' + course['name']
            cursor.execute('''
                           INSERT INTO course (prof, cid, name)
                           VALUES (%s, %s, %s);
                           ''', (prof, course_id, course_name))
            for dept in course_dept:
                cursor.execute('''
                               SELECT * FROM department
                               WHERE id=%s;
                               ''', (dept,))
                if cursor.fetchone():
                    cursor.execute('''
                                   INSERT INTO relate (course_prof, course_id, dept)
                                   VALUES (%s, %s, %s);
                                   ''', (prof, course_id, dept))

if __name__ == '__main__':
    conn = psycopg2.connect(database='',
                            user='st2957',
                            password='MWRSCW',
                            host='w4111db.eastus.cloudapp.azure.com')
    cur = conn.cursor()

    for i in range(len(dept_id)):
        res = requests.get(host_name + department_search + str(dept_id[i])).json()
        cur.execute('''
                    INSERT INTO department (id, name)
                    VALUES (%s, %s);
                    ''', (res['departments'][0]['id'], res['departments'][0]['name']))

    for i in range(len(dept_id)):
        profs = requests.get(host_name + professor_search + str(dept_id[i])).json()['professors']
        for prof in profs:
            prof_name = prof['first_name'] + ' ' + prof['last_name']
            prof_id = prof['id']
            cur.execute('''
                        SELECT * FROM professor
                        WHERE id=%s;
                        ''', (prof_id, ))
            if not cur.fetchone():
                cur.execute('''
                            INSERT INTO professor (id, name)
                            VALUES (%s, %s);
                            ''', (prof_id, prof_name))
                insert_courses(prof_id, cur)
            cur.execute('''
                        INSERT INTO affiliate (dept, prof)
                        VALUES (%s, %s);
                        ''', (dept_id[i], prof_id))
    conn.commit()
    conn.close()
