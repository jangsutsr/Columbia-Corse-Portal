CREATE TABLE usr (
    name TEXT NOT NULL,
    passwd TEXT NOT NULL,
    e_mail TEXT NOT NULL,
    PRIMARY KEY (e_mail)
);
CREATE TABLE department (
    id INTEGER NOT NULL,
    name TEXT,
    PRIMARY KEY (id)
);
CREATE TABLE professor (
    id INTEGER NOT NULL,
    name TEXT,
    PRIMARY KEY (id)
);
CREATE TABLE affiliate (
    dept INTEGER NOT NULL,
    prof INTEGER NOT NULL,
    PRIMARY KEY (dept, prof),
    FOREIGN KEY (dept) REFERENCES department (id),
    FOREIGN KEY (prof) REFERENCES professor (id)
);
-- Weak Entity [course] ==> <teach>
CREATE TABLE course (
    prof INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    name TEXT,
    workload REAL CHECK (workload < 5 AND workload >= 0),
    star REAL CHECK (star < 5 AND star >= 0),
    vote_count INTEGER,
    PRIMARY KEY (prof, cid),
    FOREIGN KEY (prof) REFERENCES professor (id)
);
CREATE TABLE subscribes (
    usr TEXT NOT NULL,
    course INTEGER NOT NULL,
    course_prof INTEGER NOT NULL,
    PRIMARY KEY (usr, course, course_prof),
    FOREIGN KEY (usr) REFERENCES usr (e_mail),
    FOREIGN KEY (course, course_prof) REFERENCES course (cid, prof)
);
CREATE TABLE relate (
    course_prof INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    dept INTEGER NOT NULL,
    PRIMARY KEY (course_prof, course_id, dept),
    FOREIGN KEY (dept) REFERENCES department (id),
    FOREIGN KEY (course_prof, course_id) REFERENCES course (prof, cid)
);
-- Aggregation [course]-<susbcribes>-[usr] 
CREATE TABLE course_subscribes_usr (
    usr TEXT NOT NULL,
    cid INTEGER NOT NULL,
    prof INTEGER NOT NULL,
    PRIMARY KEY (usr, cid, prof),
    FOREIGN KEY (usr) REFERENCES usr (e_mail),
    FOREIGN KEY (cid, prof) REFERENCES course (cid, prof)
);
-- Weak Entity [document] ==> <upload>
-- "Owned by" subscribes aggregation
CREATE TABLE document (
    did SERIAL,
    usr TEXT NOT NULL,
    cid INTEGER NOT NULL,
    prof INTEGER NOT NULL,
    name TEXT,
    file_location TEXT,
    create_date DATE,
    star REAL CHECK (star < 5 AND star >= 0),
    vote_count INTEGER CHECK (vote_count >= 0),
    report_count INTEGER CHECK (report_count >= 0),
    PRIMARY KEY (did, usr, cid, prof),
    FOREIGN KEY (usr, cid, prof) REFERENCES course_subscribes_usr
		ON DELETE CASCADE
);
-- Weak Entity [document] ==> <write>
-- "Owned by" subscribes aggregation
CREATE TABLE review (
    rid SERIAL,
    usr TEXT NOT NULL,
    cid INTEGER NOT NULL,
    prof INTEGER NOT NULL,
    content TEXT,
    create_date DATE,
    update_date DATE,
    star REAL CHECK (star < 5 AND star >= 0),
    vote_count INTEGER CHECK (vote_count >= 0),
    report_count INTEGER CHECK (report_count >= 0),
	UNIQUE (usr, cid, prof),
    PRIMARY KEY (rid, usr, cid, prof),
    FOREIGN KEY (usr, cid, prof) REFERENCES course_subscribes_usr
		ON DELETE CASCADE
);
