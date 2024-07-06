from flask import Flask, request, render_template, jsonify, redirect, url_for
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
        spots = []
        for place in response['results']:
            spot = {
                'name': place['name'],
                'image': place['photos'][0]['photo_reference'] if 'photos' in place else None
            }
            spots.append(spot)
        return spots
    else:
        return []

def get_image_url(photo_reference):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spots')
def spots():
    location = request.args.get('location')
    coords = get_coordinates(location)
    if coords:
        lat, lng = coords['lat'], coords['lng']
        spots = get_tourist_spots(lat, lng)
        for spot in spots:
            if spot['image']:
                spot['image_url'] = get_image_url(spot['image'])
        return render_template('spots.html', location=location, spots=spots)
    else:
        return render_template('error.html', message='Location not found')

if __name__ == '__main__':
    app.run(debug=True)
