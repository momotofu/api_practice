from flask import Flask, jsonify, request
import json, requests
import urllib.parse as url_parse

app = Flask(__name__)

#GET REQUEST
@app.route('/getGeocodeLocation/<input_string>')
def getGeocodeLocation(input_string):
    google_api_key = json.loads(open('./credentials.json').read())['Google'
    ' Maps API']['API Key']
    location_string = url_parse.quote(input_string)

    params = dict(
        address=location_string,
        key=google_api_key
    )
    url = ('https://maps.googleapis.com/maps/api/geocode/json')

    response = requests.get(url=url, params=params)
    data = json.loads(response.text)

    return jsonify(data)

@app.route('/readHello')
def getRequestHello():
	return "Hi, I got your GET Request!"


@app.route('/fourSquare')
def getFourSquare():
    url = 'https://api.foursquare.com/v2/venues/explore'

    credentials = json.loads(open('./credentials.json', 'r').read())['Four Square API']
    client_ID = credentials['Client ID']
    client_secret = credentials['Client Secret']

    params = dict(
        client_id=client_ID,
        client_secret=client_secret,
        v='20170801',
        ll=request.args.get('ll'),
        query=request.args.get('query'),
        limit=1
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return jsonify(data)


#POST REQUEST
@app.route('/createHello', methods = ['POST'])
def postRequestHello():
	return "I see you sent a POST message :-)"


#UPDATE REQUEST
@app.route('/updateHello', methods = ['PUT'])
def updateRequestHello():
	return "Sending Hello on an PUT request!"


#DELETE REQUEST
@app.route('/deleteHello', methods = ['DELETE'])
def deleteRequestHello():
	return "Deleting your hard drive.....haha just kidding! I received a DELETE request!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	
