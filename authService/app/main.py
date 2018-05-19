"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
"""
from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify
app = Flask(__name__)

from utilities import status_response
import dataAccess

"""
#_______________________
# Health Check          |
#_______________________|
"""
@app.route("/")
def healthCheck():
    return "authService is up and running"

"""
#_______________________
# User sign up          |
#_______________________|
"""
@app.route("/user_sign_up", methods = ['POST'])
def user_sign_up():
    status = status_response()
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if firstName and lastName and email and username and password:
            try: 
                dataAccess.lookup_email(email)
                status.set_errorMessage('email already exist')
                return status.get_response()
            except:
                try: 
                    dataAccess.lookup_username(username)
                    status.set_errorMessage('username already exist')
                    return status.get_response()
                except:
                    response = dataAccess.user_sign_up(email, password, firstName, lastName, username)
                    status.attach_data('data', response, isSuccess=True)
    return status.get_response()

"""
#___________________________
# User authenticate         |
#___________________________|
"""
@app.route("/user_authenticate", methods = ['GET'])
def user_authenticate():
    status = status_response()
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        email = request.args.get('email')
        username = request.args.get('username')
        password = request.args.get('password')
        try:
            response = dataAccess.user_authenticate(user_ID=user_ID, email=email, username=username, password=password)
            status.attach_data('data', response, isSuccess=True)
        except:
            status.set_errorMessage('email or username not exist')
    return status.get_response()

"""
#_______________________
#   Get user data       |
#_______________________|
"""
@app.route("/user_get_data", methods = ['GET'])
def user_get_data():
    status = status_response()
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        dataType = request.args.get('dataType')
        try:
            if dataType:
                response = dataAccess.user_get(user_ID, dataType=dataType)
            else:
                response = dataAccess.user_get_basic(user_ID)
            status.attach_data('data', response, isSuccess=True)
        except:
            status.set_errorMessage('user_ID not exist')
    return status.get_response()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
