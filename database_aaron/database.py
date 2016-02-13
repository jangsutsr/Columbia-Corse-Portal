import psycopg2

conn = psycopg2.connect(database='', user='st2957', password='MWRSCW', host='w4111db.eastus.cloudapp.azure.com')
cur = conn.cursor()
cur.execute('''
            CREATE TABLE usr (
                uni VARCHAR(10) NOT NULL,
                passwd TEXT NOT NULL,
                e_mail TEXT,
                perk INTEGER,
                courses TEXT[],
                PRIMARY KEY (uni)
            );
            ''')
cur.execute('''
            CREATE TABLE professor (
                uni VARCHAR(10) NOT NULL,
                name TEXT,
                e_mail TEXT,
                PRIMARY KEY (uni) );
            ''')
cur.execute('''
            CREATE TABLE course (
                cid INTEGER NOT NULL,
                uni VARCHAR(10) NOT NULL,
                name TEXT,
                star REAL,
                PRIMARY KEY (uni, cid),
                FOREIGN KEY (uni) REFERENCES professor (uni)
                    ON DELETE CASCADE
            );
            ''')
cur.execute('''
            CREATE TABLE document (
                uni VARCHAR(10) NOT NULL,
                did INTEGER NOT NULL,
                name TEXT,
                file_location TEXT,
                create_date DATE,
                star REAL,
                PRIMARY KEY (uni, did),
                FOREIGN KEY (uni) REFERENCES usr (uni)
                    ON DELETE CASCADE
            );
            ''')
cur.execute('''
            CREATE TABLE review (
                uni VARCHAR(10) NOT NULL,
                rid INTEGER NOT NULL,
                content TEXT,
                create_date DATE,
                update_date DATE,
                star REAL,
                workload INTEGER,
                PRIMARY KEY (uni, rid),
                FOREIGN KEY (uni) REFERENCES usr (uni)
                    ON DELETE CASCADE
            );
            ''')

cur.execute('''
            CREATE TABLE associate (
                usr_uni VARCHAR(10) NOT NULL,
                rid INTEGER NOT NULL,
                prof_uni VARCHAR(10) NOT NULL,
                cid INTEGER NOT NULL,
                PRIMARY KEY (usr_uni, rid, prof_uni, cid),
                FOREIGN KEY (usr_uni, rid)
                    REFERENCES review (uni, rid),
                FOREIGN KEY (prof_uni, cid)
                    REFERENCES course (uni, cid)
            );
            ''')
cur.execute('''
            CREATE TABLE contribute (
                usr_uni VARCHAR(10) NOT NULL,
                did INTEGER NOT NULL,
                prof_uni VARCHAR(10) NOT NULL,
                cid INTEGER NOT NULL,
                PRIMARY KEY (usr_uni, did, prof_uni, cid),
                FOREIGN KEY (usr_uni, did)
                    REFERENCES review (uni, did),
                FOREIGN KEY (prof_uni, cid)
                    REFERENCES course (uni, cid)
            );
            ''')
conn.commit()
conn.close()
