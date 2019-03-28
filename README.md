MiniProject for Hospital Location using a persistent Cassandra Database and an External API.

This app provides the closest distance to a hospital from any location (Postcode) in the UK using a Haversine algorithm that converts coordinates into distance.

Take a look at Miniproject.py for the specific details on the code

FOR IT TO WORK, The postcode must be written WITHOUT spaces.

****IMPORTANT***** To properly run the app, you must connect the right database, either with your local Cassandradb or a persistent database on the cloud. This can be done in lines 12-14 of the Miniproject.py file, as indicated in the code.

We will be using the APIs found on: https://api.postcodes.io to obtain the coordinates of the postcodes in the UK.

********************************************** **GENERAL SPECIFICATION**  *****************************
The purpose of the app is to find the closest hospital to your location by comparing the coordinates of you Postcode with an internal database 
We are going to perform a series of operations:

1. Create a database called Cassandra, and link it to the app on lines 12-14.

2. Launch the app.

3. Insert a postcode without spaces (Bug detected)...

4. Get the result.

What the app will do, is the following:

- Search our persistent database to find if there is a hospital on the specified postcode.

- If it is not found, then we validate that the postcode actually exists in the UK. We send a GET request to validat to the external API through a GET request.

- If it exists, then we obtain the latitude and longitude of the postcode by a new GET request to another path of the external API

- We get the latitude and longitude of the user's postcode and compare them with all the hospitals in our database.

We find the closest distance by using a haversine algorithm.

Then, we display the closest hospital to the user.



