MiniProject for Hospital Location using a persistent Cassandra Database and an External API.

This app provides the closest distance to a hospital from any location (Postcode) in the UK using a Haversine algorithm that converts coordinates into distance.

Take a look at Miniproject.py for the specific details on the code

FOR IT TO WORK, The postcode must be written WITHOUT spaces.

****IMPORTANT***** To properly run the app, you must connect the right database, either with your local Cassandradb or a persistent database on the cloud. This can be done in lines 12-14 of the Miniproject.py file, as indicated in the code.

We will be using the APIs found on: https://api.postcodes.io to obtain the coordinates of the postcodes in the UK.

************************************************GENERAL SPECITICATION******************************
The purpose of the app is to find the closest hospital to your location by comparing the coordinates of you Postcode with an internal database 
We are going to perform a series of operations:
Search our persistent database to find if there is a hospital on the specified postcode.
If it is not found, then we look for the latitude and longitude of the postcode on an external API
But first, we must validate that the postcode actually exists in the UK. We send a GET request to validate.
If successful, we perform another GET request to obtain the characteristics of the selected option
We get the latitude and lonngitude of the user's postcode and compare them with all the hospitals
We find the closest distance by using a haversine algorithm
Then, we display the closet hospital to the user.



