CREATE TABLE usr (
    uni VARCHAR(10) NOT NULL,
    passwd TEXT NOT NULL,
    e_mail TEXT,
    max_download_rate INTEGER,
    download_count INTEGER,
    courses TEXT[],
    PRIMARY KEY (uni)
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
CREATE TABLE course (
    prof INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    dept INTEGER,
    inspector VARCHAR(10),
    name TEXT,
    workload REAL,
    star REAL,
    comment_count INTEGER,
    PRIMARY KEY (prof, cid),
    FOREIGN KEY (prof) REFERENCES professor (id)
        ON DELETE CASCADE,
    FOREIGN KEY (dept) REFERENCES department (id),
    FOREIGN KEY (inspector) REFERENCES usr (uni)
);
CREATE TABLE relate (
    course_prof INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    dept INTEGER NOT NULL,
    PRIMARY KEY (course_prof, course_id, dept),
    FOREIGN KEY (dept) REFERENCES department (id),
    FOREIGN KEY (course_prof, course_id)
        REFERENCES course (prof, cid)
);
CREATE TABLE document (
    uni VARCHAR(10) NOT NULL,
    did INTEGER NOT NULL,
    name TEXT,
    file_location TEXT,
    create_date DATE,
    star REAL,
    comment_count INTEGER,
    PRIMARY KEY (uni, did),
    FOREIGN KEY (uni) REFERENCES usr (uni)
        ON DELETE CASCADE
);
CREATE TABLE review (
    uni VARCHAR(10) NOT NULL,
    rid INTEGER NOT NULL,
    content TEXT,
    create_date DATE,
    update_date DATE,
    star REAL,
    comment_count INTEGER,
    PRIMARY KEY (uni, rid),
    FOREIGN KEY (uni) REFERENCES usr (uni)
        ON DELETE CASCADE
);
