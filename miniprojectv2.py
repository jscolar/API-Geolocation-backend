from flask import Flask, render_template, request, jsonify
from cassandra.cluster import Cluster
import requests
from pprint import pprint
import json
import requests_cache
from math import radians, cos, sin, asin, sqrt

requests_cache.install_cache('postcodes_api_cache', backend='sqlite', expire_after=36000)


#cluster = Cluster(['cassandra'])
#session = cluster.connect()

app = Flask(__name__)

#************************************************GENERAL SPECITICATION******************************
#We are going to perform a series of operations:
#Search our persistent database to find if there is a hospital on the specified postcode.
#If it is not found, then we look for the latitude and longitude of the postcode on an external API
#But first, we must validate that the postcode actually exists in the UK. We send a GET request to validate.
#If successful, we perform another GET request to obtain the characteristics of the selected option
#We get the latitude and lonngitude of the user's postcode and compare them with all the hospitals
#We find the closest distance by using a haversine algorithm
#Then, we display the closet hospital to the user.

validate_postcode_template = 'https://api.postcodes.io/postcodes/{pc}/validate'
get_coordinates_template = 'https://api.postcodes.io/postcodes/{pc}'

@app.route('/')
def hello():
        name = request.args.get("name","World")
        return('<h1>Hello! Please insert the postcode on the URL path!</h1>')

@app.route('/<postcode>',  methods=['GET'])
def profile(postcode):
	validate_postcode = validate_postcode_template.format(pc = postcode)
	resp = requests.get(validate_postcode)

	if resp.ok:
		valid_pc = resp.json()
                return('RESPUESTA VALIDA. AVANZA')
#		resultado = valid_pc['result']
#		pprint(resultado)
#
#		if resultado != 'false':
#			get_coordinates = get_coordinates_template.format(pc = postcode)
#			resp2 = requests.get(get_coordinates)
#
#			if resp2.ok:
#				pc_details = resp2.json()
#				latu = pc_details['result'].get('latitude')
#				lonu = pc_details['result'].get('longitude')
#				pprint(pc_details)
#				return('The latitude is {} and the longitude is {}'.format(latu, lonu))
#			else:
#				print(resp2.reason)
#				return('404. The postcode is not registered in the UK. Please try again')
#		else:
#			return('404. The postcode is not registered in the UK. Please try again')

	else:
		return('500. There is an error in the system. Please try later')



#@app.route('/hospital/<postal>/')
#def profile(city):
#	rows = session.execute("Select * From hospital.stats where city = '{}'".format(city))

#	for hospital in rows:
#		return('<h1>{} is in {}, located in {}!</h1>'.format(hospital.organisationname, city, hospital.postcode))
#	return('<h1>This city has no registered hospitals!</h1>')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)


