-- How many Professors are affiliated with the CS department?

SELECT COUNT(P.id)
FROM professor P, affiliate A
WHERE P.id = A.prof AND A.dept = 7;

-- What are the names of the students who have written a review or uploaded a document?

SELECT DISTINCT U.name
FROM usr U, review R, document D
WHERE U.e_mail = R.usr AND U.e_mail = D.usr;

-- What are the names of the Professors who have classes with both reviews and documents associated with them?

SELECT P.name
FROM professor P
WHERE P.id IN (SELECT DISTINCT D.prof
              FROM course C, document D
              WHERE C.cid = D.cid
		      INTERSECT
			  SELECT DISTINCT R.prof
			  FROM course C, review R
			  WHERE C.cid = R.cid
		      );

