from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyC6JXdrY5SNL31rPWL1RUrln15ymEolLWQ'

def get_coordinates(location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    response = requests.get(url).json()
    if response['status'] == 'OK':
        return response['results'][0]['geometry']['location']
    else:
        return None

def get_tourist_spots(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=tourist_attraction&key={API_KEY}"
    response = requests.get(url).json()
    if response['status'] == 'OK':
        return [place['name'] for place in response['results']]
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_spots', methods=['POST'])
def get_spots():
    data = request.json
    location = data['location']
    coords = get_coordinates(location)
    if coords:
        lat, lng = coords['lat'], coords['lng']
        spots = get_tourist_spots(lat, lng)
        return jsonify({'lat': lat, 'lng': lng, 'spots': spots})
    else:
        return jsonify({'error': 'Location not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
