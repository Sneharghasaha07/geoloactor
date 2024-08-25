from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from geopy.distance import geodesic
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace with your actual site's latitude and longitude
SITE_LOCATION = (22.052811127784658, 88.1056873601272)
RADIUS_METERS = 1000
TIME_LIMIT_MINUTES = 30

# Dummy user data
USERS = {
    'admin': 'password123'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Authentication failed!"
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add logic to save the new user credentials
        USERS[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        current_location = (latitude, longitude)

        # Calculate the distance
        distance = geodesic(current_location, SITE_LOCATION).meters

        # Print current location and distance to the terminal
        print(f"Current location: Latitude = {latitude}, Longitude = {longitude}")
        print(f"Distance from site: {distance} meters")

        if is_within_site(current_location, SITE_LOCATION, RADIUS_METERS):
            session['start_time'] = datetime.now().isoformat()  # Store start time as ISO format string
            return redirect(url_for('data_entry'))
        else:
            return "Not within site. Access to update data denied."

    return render_template('entry.html')

@app.route('/distance', methods=['POST'])
def distance():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    current_location = (latitude, longitude)

    # Calculate the distance
    distance = geodesic(current_location, SITE_LOCATION).meters

    return jsonify({'distance': distance})

@app.route('/data_entry', methods=['GET', 'POST'])
def data_entry():
    if 'username' not in session or 'start_time' not in session:
        return redirect(url_for('login'))

    start_time = datetime.fromisoformat(session['start_time'])  # Convert ISO format string back to datetime
    if datetime.now() > start_time + timedelta(minutes=TIME_LIMIT_MINUTES):
        return "Time limit exceeded. Access to update data denied."

    if request.method == 'POST':
        # Handle data entry
        data = request.form['data']
        # Save data to the database or process it here
        return "Data updated successfully!"

    return render_template('data_entry.html')

def is_within_site(current_location, site_location, radius_meters):
    distance = geodesic(current_location, site_location).meters
    return distance <= radius_meters

if __name__ == '__main__':
    app.run(debug=True)
