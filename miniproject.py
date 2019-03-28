from flask import Flask, render_template, request, jsonify
from cassandra.cluster import Cluster
import requests
from pprint import pprint
import json
import requests_cache
from math import radians, cos, sin, asin, sqrt

requests_cache.install_cache('postcodes_api_cache', backend='sqlite', expire_after=36000)

#Use line 12 to connect to a persistent database and comment line 14
#cluster = Cluster(['cassandra'])
#Use line 14 to connect to a local database, with an IP Address and comment line 12.
cluster = Cluster(['172.18.0.2'])
session = cluster.connect()

app = Flask(__name__)

#************************************************GENERAL SPECITICATION******************************
#The purpose of the app is to find the closest hospital to your location by comparing the coordinates of you Postcode with an internal database 
#We are going to perform a series of operations:
#Search our persistent database to find if there is a hospital on the specified postcode.
#If it is not found, then we look for the latitude and longitude of the postcode on an external API
#But first, we must validate that the postcode actually exists in the UK. We send a GET request to validate.
#If successful, we perform another GET request to obtain the characteristics of the selected option
#We get the latitude and lonngitude of the user's postcode and compare them with all the hospitals
#We find the closest distance by using a haversine algorithm
#Then, we display the closet hospital to the user.

#Here, we can find the APIs:
validate_postcode_template = 'https://api.postcodes.io/postcodes/{pc}/validate'
get_coordinates_template = 'https://api.postcodes.io/postcodes/{pc}'

#This route displays a general form to insert the Postcode:
@app.route('/')
def hello():
	return(render_template('my_form.html'))


#This route takes the output of the form and performs the operations:
@app.route('/',  methods=['GET','POST'])
def profile():
	text = request.form['postcode']
	post1 = text.upper()
	postcode = post1.replace(" ", "")
	pprint(postcode)


#We first compare the user postode with our persistent database:
	rows = session.execute("""SELECT * FROM hospital.stats WHERE Postcode = '{}'ALLOW FILTERING""".format(postcode))

	for hospital in rows:
		name = hospital.organisationname
		address = hospital.address1
		address2 = hospital.address2
		return('There is a match! {} is located in {} and {}'.format(name, address, address2))

	response = []
#If there is a response, we store it in an array, and provide the answer to the user:
	for row in rows:
		response.append(row)
	if len(response)>0:
		return('There is a match! {} is located in {} and {}'.format(name, address, address2))
	else:

#If we found no answer, then we validate that the postcode actually exists. We look at an external API to do this by sending a GET request:
		validate_postcode = validate_postcode_template.format(pc = postcode)
		resp = requests.get(validate_postcode)

		if resp.ok:
			valid_pc = resp.json()
			resultado = valid_pc['result']
			pprint(resultado)

#If the postcode exists, then we send another request to ask for its coodinates:
			if resultado != 'false':
				get_coordinates = get_coordinates_template.format(pc = postcode)
				resp2 = requests.get(get_coordinates)

#We store the coordinates in two variables, latitude and longitude:

				if resp2.ok:
					pc_details = resp2.json()
					latu = pc_details['result'].get('latitude')
					lonu = pc_details['result'].get('longitude')
					float(latu)
					float(lonu)
					pprint(pc_details)
					lonu, latu = map(radians, [lonu, latu])
					min = 5000

#We compare them with every hospital registered in the database, and then, find the minimum distance:
					question = session.execute("""SELECT * FROM hospital.stats WHERE latitude > 1 ALLOW FILTERING""")
					for hospitales in question:
						lath = hospitales.latitude
						lonh = hospitales.longitude
						lonh, lath = map(radians, [lonh, lath])
						dlon = lonh - lonu
						dlat = lath - latu
						a = sin(dlat/2)**2 + cos(latu) * cos(lath) * sin(dlon/2)**2
						c = 2 * asin(sqrt(a))
						r = 6371
						distance = r*c
#						pprint(distance)
						pprint(min)
						if distance<min:
							min = distance
							name = hospitales.organisationname
							address = hospitales.address1
							address2 = hospitales.address2
							city = hospitales.city
					return('The closest hospital to {} is {}, located {} KM away in {} {}, {}'.format(postcode, name, min, address, address2, city))

#If the code was not found, it sends a 404 response:
				else:
					print(resp2.reason)
					return('404. The postcode is not registered in the UK. Please try again')
			else:
				return('404. The postcode is not registered in the UK. Please try again')
#If there was an error with the API, then a 500 code is displayed:
		else:
			return('500. There is an error in the system. Please try later')



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)


