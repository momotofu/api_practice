from flask import Flask, jsonify, request
import json, requests
import urllib.parse as url_parse

import sys
import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

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
    location = data['results'][0]['geometry']['location']
    longitude = location['lng']
    latitude = location['lat']

    ll = dict(
        longitude=longitude,
        latitude=latitude
    )

    return jsonify(ll)


@app.route('/findRestaurant')
def findRestaurant(address="Osaka", query="ramen"):
    if 'address' in request.args:
        address = request.args.get('address')
    if 'query' in request.args:
        query = request.args.get('query')

    ll_data = json.loads(getGeocodeLocation(address).data.decode())
    ll = ll_data['latitude'], ll_data['longitude']
    print('ll: ', ll.data.decode())
    response = json.loads(getFourSquare(query, ll).data.decode())
    print('response: ', response)


@app.route('/fourSquare')
def getFourSquare(query='pizza', ll='Osaka'):
    url = 'https://api.foursquare.com/v2/venues/explore'

    if 'query' in request.args:
        query = request.args.get('query')
    if 'll' in request.args:
        ll = request.args.get('ll')

    credentials = json.loads(open('./credentials.json', 'r').read())['Four Square API']
    client_ID = credentials['Client ID']
    client_secret = credentials['Client Secret']

    params = dict(
        client_id=client_ID,
        client_secret=client_secret,
        v='20170801',
        ll=ll,
        query=query,
        limit=5
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return jsonify(data)


if __name__ == '__main__':
    print('test')
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
