from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify

import dbAccess
import addressInterpretor
app = Flask(__name__)

"""
#_______________________
# Health Check          |
#_______________________|
"""
@app.route("/")
def healthCheck():
    return "attractionService is up and running"

@app.route("/create_attraction")
def create_attraction():
    status = status_response()
    if request.method == 'POST':
        user_ID = request.form.get('user_ID')
        name = request.form.get('name')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        intro = request.form.get('intro')
        address = addressInterpreter.gps_to_address(latitude = float(latitude), longitude = float(longitude))
        
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
