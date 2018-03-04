ASSUMPTIONS MADE:
  1. 2 Points are said to lie too close to each other when they within a radius of 3-4 Kms of each other.
  2. We are operating on a databse named : 'jimmy', handled by username : 'jimmy' with password : 'hello123'
  3. The database consists of table named record consisting of the followinf columns :
     key : varchar
     place : varchar
     admin_name1 : varchar
     latitude : real
     longitude : real
     accuracy : integer
     checker : false (this column was introduced by mean to tackle Interview Question 2)



--Interview Question 1--
The POST api : "/post_location" asks the user to fill up a form giving details of the Pincode, Address, City, Longitude and Latitude.

We check if the given pin-code already exists in the database, or the the long/lat give lie in the range of 3-4Kms of any other coordinate? If yes, then the given location is NOT added. Else, Added!


--Interview Question 2--
The GET api takes the details from the user and displays all locations lying in the specified region.

This API has been implemented using 2 different methods :
1. using 'earthdistance' : "/get_using_postgres",
   This method makes the uses of earth_distance extension of Postgresql and prints the desired list. I made the use of         
   psycopg2.connect() to connect to a given database and execute SQL commands directly from the IDE.
   
2. using Mathematical Computation : "get_using_self",
   I used Haversine formula to compute the distance between 2 given longitudes and latitudes.
   
   
   
