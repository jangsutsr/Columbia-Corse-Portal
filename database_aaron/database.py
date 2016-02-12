import psycopg2

conn = psycopg2.connect(database='', user='st2957', password='MWRSCW', host='w4111db.eastus.cloudapp.azure.com')
cur = conn.cursor()
cur.execute('''
            CREATE TABLE usr (
                uni VARCHAR(10) NOT NULL,
                name VARCHAR(100),
                passwd TEXT NOT NULL,
                e_mail TEXT,
                perk INTEGER,
                courses_taken INTEGER[],
                PRIMARY KEY (uni)
            );
            ''')
cur.execute('''
            CREATE TABLE inspector (
                -- Foreigns
                uni VARCHAR(10) NOT NULL,
                -- Locals
                countdown INTEGER,
                max_course_number INTEGER,
                PRIMARY KEY (uni),
                FOREIGN KEY (uni) REFERENCES user
            );
            ''')
cur.execute('''

CREATE TABLE client (
	-- Foreigns
	uni VARCHAR(10) NOT NULL,
	-- Locals
	max_download_rate INTEGER,
	max_upload_rate INTEGER,
	PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES user );

            ''')
conn.commit()
conn.close()
