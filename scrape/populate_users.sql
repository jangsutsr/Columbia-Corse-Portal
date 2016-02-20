-- INSERTS for Project 1 Part 2

-- Relations populated by Aaron's Python script:
-- course, relate, affiliate, prof, dept

-- Relations populated manually by Walt (this sql file):
-- usr, take, document, review

-- usr
INSERT INTO usr (name, passwd, e_mail) VALUES
    ('Walter Meyer', 'notsecurepassword123', 'wgm2110@columbia.edu'),
    ('Sirui Tan', 'badpassword321', 'st2957@columbia.edu'),
    ('Boyu Wang', 'badpassword321','bw2387@columbia.edu');

-- take
INSERT INTO subscribes (usr, course, course_prof) VALUES
    ('wgm2110@columbia.edu', '4758', '12357'),
	('wgm2110@columbia.edu', '6511', '12620'),
	('wgm2110@columbia.edu', '6362', '11574'),
    ('st2957@columbia.edu', '4758', '12357'),
	('st2957@columbia.edu', '397', '11575'),
	('st2957@columbia.edu', '6362', '11574'),
    ('st2957@columbia.edu', '2906', '10725'),
	('bw2387@columbia.edu', '4758', '12357'),
	('bw2387@columbia.edu', '2906', '10725'),
    ('bw2387@columbia.edu', '2830', '2089'),
	('bw2387@columbia.edu', '2387', '47'),
	('bw2387@columbia.edu', '5150', '1777');

-- course_subscribes_usr
INSERT INTO course_subscribes_usr (usr, cid, prof) VALUES
	('wgm2110@columbia.edu', '4758', '12357'),
	('wgm2110@columbia.edu', '6511', '12620'),
	('wgm2110@columbia.edu', '6362', '11574'),
	('st2957@columbia.edu', '4758', '12357'),
	('bw2387@columbia.edu', '2830', '2089');

-- document
INSERT INTO document (usr, cid, prof, name, file_location, 
					create_date) VALUES
	('wgm2110@columbia.edu', '4758', '12357', 'Syllabus', 
	 '/documents/12357-4758/syllabus.pdf', '2014-10-05'),
 	('st2957@columbia.edu', '4758', '12357', 'Homework',
	 '/documents/12357-4758/hw1.pdf', '2016-01-05'),
 	('bw2387@columbia.edu', '2830', '2089', 'Study Guide Latest',
	 '/documents/12357-4758/studyguide.pdf', '2015-11-15');

-- review
INSERT INTO review (usr, cid, prof, content, create_date, star, vote_count, report_count) VALUES
	('wgm2110@columbia.edu', '4758', '12357',
	 'This class was the greatest class ever. I am a better person because of it.',
	'2014-10-05', '5.0', '5', '1'),
	('wgm2110@columbia.edu', '6511', '12620',
	 'This class was the worst class ever. I am a terrible person because of it.',
	'2014-12-25', '1.0', '1', '1'),
	('wgm2110@columbia.edu', '6362', '11574',
	 'This class was mediocre. Too much homework.',
	'2016-01-05', '3.0', '3', '1'),
	--
	('st2957@columbia.edu', '4758', '12357',
	 'This class was wonderful. Teacher was great!',
	'2016-01-05', '4.5', '4', '2'),
	--
	('bw2387@columbia.edu', '2830', '2089',
	 'This class was fantastic. I loved the lectures!',
	'2016-01-05', '5.0', '5', '1');
