-- Entities
CREATE TABLE cu_er (
    uni VARCHAR(10),
    name VARCHAR(100),
    passwd TEXT,
    e_mail TEXT,
    perk INTEGER,
    courses_taken VARCHAR(15),
    PRIMARY KEY (uni) );

CREATE TABLE inspector (
	uni VARCHAR(10),
	countdown INTEGER,
	max_course_number INTEGER,
	PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES cu_er );

CREATE TABLE client (
	uni VARCHAR(10),
	max_download_rate INTEGER,
	max_upload_rate INTEGER,
	PRIMARY KEY (uni),
	FOREIGN KEY (uni) REFERENCES cu_er );

CREATE TABLE course_permit_instruct (
	professor_id VARCHAR(10),
	id VARCHAR(15),
	star REAL,
	doc_permission BOOLEAN,
	workload REAL,
	name TEXT,
	update_date TIMESTAMP,
	student_list TEXT[],
	max_inspector_number INTEGER,
	PRIMARY KEY (professor_id, id),
	FOREIGN KEY (professor_id) REFERENCES professor
		ON DELETE CASCADE);

CREATE TABLE document_delete_upload (
	contributer VARCHAR(10),
	id INTEGER,
	prof VARCHAR(10),
	course_prof_id VARCHAR(10),
	course_id VARCHAR(15),
	name TEXT,
	tags TEXT[],
	inspectors TEXT[],
	votes INTEGER,
	create_date TIMESTAMP,
	publish_date TIMESTAMP,
	raw_file TEXT,
	PRIMARY KEY (contributer, id),
	FOREIGN KEY (contributer) REFERENCES client
		ON DELETE CASCADE,
	FOREIGN KEY (course_prof_id, course_id) REFERENCES course_permit_instruct,
	FOREIGN KEY (prof) REFERENCES professor);

CREATE TABLE review_write (
	writer VARCHAR(10),
	id INTEGER,
	course_prof_id VARCHAR(10),
	course_id VARCHAR(15),
	inspectors TEXT[],
	votes INTEGER,
	create_date TIMESTAMP,
	publish_date TIMESTAMP,
	update_date TIMESTAMP,
	content TEXT,
	workload REAL,
	PRIMARY KEY (writer, id),
	FOREIGN KEY (writer) REFERENCES client
		ON DELETE CASCADE
	FOREIGN KEY (course_prof_id, course_id) REFERENCES course_permit_instruct);

CREATE TABLE professor(
	uni VARCHAR(10),
	e_mail TEXT,
	PRIMARY KEY (uni) );

-- Relations
CREATE TABLE responsible_for(
	course_prof_id VARCHAR(10) NOT NULL,
	course_id VARCHAR(15) NOT NULL,
	course_inspector_uni VARCHAR(10) NOT NULL,
	PRIMARY KEY (course_prof_id, course_id, course_inspector_uni),
	FOREIGN KEY (course_prof_id, course_id) REFERENCES course_permit_instruct,
	FOREIGN KEY (course_inspector_uni) REFERENCES inspector);

CREATE TABLE inspect_doc(
	inspector_uni VARCHAR(10),
	doc_contributer VARCHAR(10) NOT NULL,
	doc_id INTEGER NOT NULL,
	PRIMARY KEY (inspector_uni, doc_contributer, doc_id),
	FOREIGN KEY (inspector_uni) REFERENCES inspector,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_delete_upload);

CREATE TABLE inspect_review(
	inspector_uni VARCHAR(10),
	review_writer VARCHAR(10) NOT NULL,
	review_id INTEGER NOT NULL,
	PRIMARY KEY (inspector_uni, review_writer, review_id),
	FOREIGN KEY (inspector_uni) REFERENCES inspector, 
	FOREIGN KEY (review_writer, review_id) REFERENCES review_write);

CREATE TABLE report_on(
	client_uni VARCHAR(10),
	doc_contributer VARCHAR(10),
	doc_id INTEGER,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_delete_upload);

CREATE TABLE vote_doc(
	client_uni VARCHAR(10),
	doc_contributer VARCHAR(10),
	doc_id INTEGER,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_delete_upload);

CREATE TABLE download( 
	client_uni VARCHAR(10),
	doc_contributer VARCHAR(10),
	doc_id INTEGER,
	PRIMARY KEY (client_uni, doc_contributer, doc_id),
	FOREIGN KEY (client_uni) REFERENCES client,
	FOREIGN KEY (doc_contributer, doc_id) REFERENCES document_delete_upload);

CREATE TABLE vote_review(
	client_uni VARCHAR(10),
	review_writer VARCHAR(10),
	review_id INTEGER,
	PRIMARY KEY (client_uni, review_writer, review_id),
	FOREIGN KEY (client_uni) REFERENCES client,
	FOREIGN KEY (review_writer, review_id) REFERENCES client);


