-- Entities
CREATE TABLE usr (
    uni VARCHAR(10) NOT NULL,
    passwd TEXT NOT NULL,
    e_mail TEXT UNIQUE,
    max_download_rate INTEGER,
    download_count INTEGER,
    PRIMARY KEY (uni)
);
CREATE TABLE professor (
    uni VARCHAR(10) NOT NULL,
    PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES usr (uni)
);
-- Weak entity
CREATE TABLE course_teach (
	-- prof
    prof_uni VARCHAR(10) NOT NULL UNIQUE,
	-- locals
    cid serial,
	dep TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    workload REAL,
    star REAL,
    FOREIGN KEY (prof_uni) REFERENCES professor (uni),
    PRIMARY KEY (cid)
);
-- Weak entity
CREATE TABLE document_upload (
	-- usr
    uploader_uni VARCHAR(10) NOT NULL,
	-- course_teach
	doc_cid INTEGER NOT NULL,
	-- locals
    did serial,
    name TEXT,
    file_location TEXT,
    date DATE,
    star REAL,
    FOREIGN KEY (uploader_uni) REFERENCES usr (uni),
    FOREIGN KEY (doc_cid) REFERENCES course_teach (cid),
	PRIMARY KEY (did)
);
-- Weak entity
CREATE TABLE review_write (
	-- one review per course per user
	-- usr
    reviewer_uni VARCHAR(10) NOT NULL UNIQUE,
	-- course_teach
	review_cid INTEGER NOT NULL UNIQUE,
	-- locals
    rid serial,
    content TEXT,
    create_date DATE,
    update_date DATE,
    star REAL,
    FOREIGN KEY (reviewer_uni) REFERENCES usr (uni),
	FOREIGN KEY (review_cid) REFERENCES course_teach (cid),
    PRIMARY KEY (rid)
);
-- Relations
CREATE TABLE takes (
	-- course_teach
    cid INTEGER NOT NULL,
	-- usr
    usr_uni VARCHAR(10) NOT NULL,
 	FOREIGN KEY (usr_uni) REFERENCES usr (uni),
	FOREIGN KEY (cid) REFERENCES course_teach (cid),
	PRIMARY KEY (cid, usr_uni)
);
CREATE TABLE report_doc (
	-- usr
    uni VARCHAR(10) NOT NULL,
	-- document_upload
    did INTEGER NOT NULL,
	-- locals
    date DATE,
    FOREIGN KEY (uni) REFERENCES usr (uni),
    FOREIGN KEY (did) REFERENCES document_upload (did),
	-- a user can only report a given doc once
	PRIMARY KEY (uni, did)
);
CREATE TABLE report_review (
	-- usr
    uni VARCHAR(10) NOT NULL,
	-- review_write
    rid INTEGER NOT NULL,
	-- locals
    date DATE,
    FOREIGN KEY (uni) REFERENCES usr (uni),
    FOREIGN KEY (rid) REFERENCES review_write (rid),
	-- a user can only report a given review once
	PRIMARY KEY (uni, rid)
);
