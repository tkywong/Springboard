/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */


/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */

******************************************
SELECT name, membercost
FROM country_club.Facilities
WHERE membercost >0
******************************************

/* Q2: How many facilities do not charge a fee to members? */

******************************************
SELECT 	COUNT(membercost)
FROM 	country_club.Facilities
WHERE	membercost = 0
******************************************

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

******************************************
SELECT facid, name, membercost, monthlymaintenance
FROM country_club.Facilities
WHERE membercost >0
AND membercost < (monthlymaintenance*0.2)
******************************************

/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */

******************************************
SELECT *
FROM country_club.Facilities
WHERE facid BETWEEN 1 AND 5 AND facid <> 2 AND facid <> 3 AND facid <> 4
******************************************

OR 
******************************************
SELECT *
FROM country_club.Facilities
WHERE facid IN (1,5)
******************************************

/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */

******************************************
SELECT 	name, monthlymaintenance,
       	CASE WHEN monthlymaintenance > 100 THEN 'EXPENSIVE'
	ELSE 'CHEAP' END AS 'CHEAP OR EXPENSIVE?'
FROM 	country_club.Facilities
******************************************


/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */

******************************************
SELECT 	firstname, surname, joindate
FROM 	country_club.Members
WHERE joindate = (SELECT MAX(joindate) FROM country_club.Members)
******************************************

/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

******************************************
SELECT DISTINCT concat(firstname, ' ' ,surname) as full_name, 'Tennis Court' as Court
FROM country_club.Bookings booking
JOIN country_club.Members member ON booking.memid = member.memid
JOIN country_club.Facilities facil ON booking.facid = facil.facid
WHERE name LIKE 'Tennis Court%' AND firstname <> 'GUEST'
GROUP BY full_name
ORDER BY full_name
******************************************

/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

******************************************
SELECT starttime,name, concat(firstname, ' ' ,surname) as full_name,
CASE WHEN member.memid > 0 THEN membercost*slots ELSE guestcost*slots END AS cost
FROM country_club.Bookings book
JOIN country_club.Facilities facil ON book.facid = facil.facid
JOIN country_club.Members member ON book.memid = member.memid
HAVING starttime LIKE '2012-09-14%' AND cost > 30
ORDER BY cost desc
******************************************

/* Q9: This time, produce the same result as in Q8, but using a subquery. */

******************************************
SELECT a1.name, a1.full_name, a1.cost

FROM
(SELECT starttime,name, concat(firstname, ' ' ,surname) as full_name,
CASE WHEN member.memid > 0 THEN membercost*slots ELSE guestcost*slots END AS cost
FROM country_club.Bookings book
JOIN country_club.Facilities facil ON book.facid = facil.facid
JOIN country_club.Members member ON book.memid = member.memid
WHERE starttime LIKE '2012-09-14%'
ORDER BY cost desc) as a1

WHERE cost > 30
******************************************

/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

******************************************
SELECT a1.name,
sum(a1.cost) as total_revenue

FROM
(SELECT name, member.memid, membercost, guestcost,
CASE WHEN member.memid > 0 THEN membercost*slots ELSE guestcost*slots END AS cost
FROM country_club.Bookings book
JOIN country_club.Facilities facil ON book.facid = facil.facid
JOIN country_club.Members member ON book.memid = member.memid) as a1

GROUP BY a1.name
HAVING total_revenue < 1000
******************************************

















