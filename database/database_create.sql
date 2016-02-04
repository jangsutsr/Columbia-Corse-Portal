-- Entities
CREATE TABLE professor(
	uni VARCHAR(10) NOT NULL,
	e_mail TEXT,
	PRIMARY KEY (uni) );

CREATE TABLE user (
    uni VARCHAR(10) NOT NULL,
    name VARCHAR(100),
    passwd TEXT NOT NULL,
    e_mail TEXT,
    perk INTEGER,
    courses_taken INTEGER[],
    PRIMARY KEY (uni) );

CREATE TABLE inspector (
	-- Foreigns
	uni VARCHAR(10) NOT NULL,
	-- Locals
	countdown INTEGER,
	max_course_number INTEGER,
	PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES user );

CREATE TABLE client (
	-- Foreigns
	uni VARCHAR(10) NOT NULL,
	-- Locals
	max_download_rate INTEGER,
	max_upload_rate INTEGER,
	PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES user );

-- Weak Entities
CREATE TABLE course_instruct (
	-- Foreigns
	prof_uni VARCHAR(10) NOT NULL,
	-- Locals
	course_id VARCHAR(15) NOT NULL,
	star REAL,
	doc_permission BOOLEAN,
	workload REAL,
	name TEXT,
	update_date TIMESTAMP,
	student_list TEXT[],
	max_inspector_number INTEGER,
	PRIMARY KEY (prof_uni, course_id),
	FOREIGN KEY (prof_uni) REFERENCES professor (uni) ON DELETE CASCADE);

CREATE TABLE document_upload (
	-- Foreigns
	contributer VARCHAR(10) NOT NULL,
	course_prof VARCHAR(10) NOT NULL,
	course_id VARCHAR(15) NOT NULL,
	-- Locals
	doc_id INTEGER NOT NULL,
	name TEXT,
	tags TEXT[],
	inspectors TEXT[],
	votes INTEGER,
	create_date TIMESTAMP,
	publish_date TIMESTAMP,
	raw_file TEXT,
	PRIMARY KEY (contributer, doc_id, course_prof, course_id),
	FOREIGN KEY (contributer) REFERENCES client (uni) ON DELETE CASCADE,
	FOREIGN KEY (course_prof, course_id) REFERENCES course_instruct (prof_uni, course_id));

CREATE TABLE review_write (
	-- Foreigns
	writer VARCHAR(10) NOT NULL,
	course_prof VARCHAR(10) NOT NULL,
	course_id VARCHAR(15) NOT NULL,
	-- Locals
	id INTEGER NOT NULL,
	inspectors TEXT[],
	votes INTEGER,
	create_date TIMESTAMP,
	publish_date TIMESTAMP,
	update_date TIMESTAMP,
	content TEXT,
	workload REAL,
	PRIMARY KEY (writer, id, course_prof, course_id),
	FOREIGN KEY (writer) REFERENCES client (uni) ON DELETE CASCADE,
	FOREIGN KEY (course_prof, course_id) REFERENCES course_instruct (prof_uni, course_id));

-- Relations
CREATE TABLE permit_course (
	course_prof VARCHAR(10) NOT NULL,
	course_id VARCHAR(15) NOT NULL,
	prof_uni VARCHAR(10) NOT NULL,
	UNIQUE (course_prof, course_id),
	PRIMARY KEY (course_prof, course_id, prof_uni),
	FOREIGN KEY (course_prof, course_id) REFERENCES course_instruct (prof_uni, course_id),
	FOREIGN KEY (prof_uni) REFERENCES professor (uni));

CREATE TABLE delete_doc (
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	prof_uni VARCHAR(10) NOT NULL,
	UNIQUE (prof_uni, doc_id),
	PRIMARY KEY (doc_contributer, doc_id, prof_uni),
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_upload (contributer, doc_id),
	FOREIGN KEY (prof_uni) REFERENCES professor (uni));

CREATE TABLE cover_course(
	course_prof_id VARCHAR(10) NOT NULL,
	course_id VARCHAR(15) NOT NULL,
	course_inspector_uni VARCHAR(10) NOT NULL,
	PRIMARY KEY (course_prof_id, course_id, course_inspector_uni),
	FOREIGN KEY (course_prof_id, course_id) REFERENCES course_instruct (prof_uni, course_id),
	FOREIGN KEY (course_inspector_uni) REFERENCES inspector (uni));

CREATE TABLE inspect_doc(
	inspector_uni VARCHAR(10) NOT NULL,
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	PRIMARY KEY (inspector_uni, doc_contributer, doc_id),
	FOREIGN KEY (inspector_uni) REFERENCES inspector,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_upload (contributer, doc_id));

CREATE TABLE inspect_review(
	inspector_uni VARCHAR(10) NOT NULL,
	review_writer VARCHAR(10) NOT NULL,
	review_id INTEGER NOT NULL,
	PRIMARY KEY (inspector_uni, review_writer, review_id),
	FOREIGN KEY (inspector_uni) REFERENCES inspector (uni), 
	FOREIGN KEY (review_writer, review_id) REFERENCES review_write (writer, id));

CREATE TABLE report_doc(
	client_uni VARCHAR(10) NOT NULL,
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client (uni),
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_upload (contributer, doc_id));

CREATE TABLE vote_doc(
	client_uni VARCHAR(10) NOT NULL,
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_upload (contributer, doc_id));

CREATE TABLE download_doc( 
	client_uni VARCHAR(10) NOT NULL,
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client (uni),
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_upload (contributer, doc_id));

CREATE TABLE vote_review(
	client_uni VARCHAR(10) NOT NULL,
	review_writer VARCHAR(10) NOT NULL,
	review_id INTEGER NOT NULL,
	PRIMARY KEY (client_uni, review_writer, review_id),
	FOREIGN KEY (client_uni) REFERENCES client (uni),
	FOREIGN KEY (review_writer, review_id) REFERENCES review_write (contributer, doc_id));

