from flask import Flask
app = Flask(__name__)

from utilities import status_response
import dataAccess

@app.route("/")
def healthCheck():
    return "authService is up and running"

@app.route("/user_sign_up", methods = ['POST'])
def user_sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        dataAccess.user_sign_up(email, password, firstName, lastName, username)

@app.route("/user_authenticate", methods = ['GET'])
def user_authenticate():
    status = status_response()
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        email = request.args.get('email')
        username = request.args.get('username')
        password = request.args.get('password')
        response = dataAccess.user_authenticate(user_ID=user_ID, email=email, username=username, password=password)
        if response:
            status.set_status = True
    return status.get_response()

@app.route("/user_get_data", methods = ['GET'])
def user_get_data():
    status = status_response()
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        dataType = request.args.get('dataType')
        if dataType:
            response = dataAccess.user_get(user_ID, dataType=dataType)
        else:
            response = dataAccess.user_get_basic(user_ID)
        status.attach_data('data', response, isSuccess=True)
    return status.get_response()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
