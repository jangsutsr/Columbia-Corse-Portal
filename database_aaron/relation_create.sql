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
CREATE TABLE contribute (
    usr_uni VARCHAR(10) NOT NULL,
    did INTEGER NOT NULL,
    prof_uni VARCHAR(10) NOT NULL,
    cid INTEGER NOT NULL,
    PRIMARY KEY (usr_uni, did, prof_uni, cid),
    FOREIGN KEY (usr_uni, did)
        REFERENCES document (uni, did),
    FOREIGN KEY (prof_uni, cid)
        REFERENCES course (uni, cid)
);
CREATE TABLE inspect_doc (
    uni VARCHAR(10) NOT NULL,
    doc_owner VARCHAR(10) NOT NULL,
    did INTEGER NOT NULL,
    inspect_date DATE,
    UNIQUE (doc_owner, did),
    PRIMARY KEY (uni, doc_owner, did),
    FOREIGN KEY (uni) 
        REFERENCES usr (uni),
    FOREIGN KEY (doc_owner, did)
        REFERENCES document (uni, did)
);
CREATE TABLE inspect_review (
    uni VARCHAR(10) NOT NULL,
    rev_author VARCHAR(10) NOT NULL,
    rid INTEGER NOT NULL,
    inspect_date DATE,
    UNIQUE (rev_author, rid),
    PRIMARY KEY (uni, rev_author, rid),
    FOREIGN KEY (uni) 
        REFERENCES usr (uni),
    FOREIGN KEY (rev_author, rid)
        REFERENCES review (uni, rid)
);
CREATE TABLE delete_doc (
    uni VARCHAR(10) NOT NULL,
    doc_owner VARCHAR(10) NOT NULL,
    did INTEGER,
    PRIMARY KEY (uni, doc_owner, did),
    FOREIGN KEY (uni)
        REFERENCES professor (uni),
    FOREIGN KEY (doc_owner, did)
        REFERENCES document (uni, did)
);
