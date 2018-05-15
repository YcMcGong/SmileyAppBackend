"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________

"""
from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify
from utilities import status_response
import dataAccess
import notifyMap

app = Flask(__name__)

"""
#  ________________________________________
# |Health Check                            |
# |________________________________________|
"""
@app.route("/")
def healthCheck():
    return "relationService is up and running"

"""
#  ________________________________________
# |Friend Management                       |
# |________________________________________|
"""
@app.route("/add_follow", methods = ['POST'])
def add_follow():
    status = status_response()
    if request.method == 'POST':
        from_user = request.form.get('from_user')
        to_user = request.form.get('to_user')
        # add follow to database
        response = dataAccess.add_follow(from_user, to_user)
        if response:
            # get a list of moment dicts needed to be propagated
            momentDictList = dataAccess.get_moments(to_user)
            if momentDictList:
                response = notifyMap.followPropagate(momentDictList, from_user)
                if response:
                    status.set_status(True)
                else:
                    status.set_errorMessage('failed to notify map')
            else:
                status.set_status(True)
                status.set_errorMessage('this user has no moments')
    return status.get_response()

@app.route("/delete_follow", methods = ['DELETE'])
def delete_follow():
    status = status_response()
    if request.method == 'DELETE':
        from_user = request.form.get('from_user')
        to_user = request.form.get('to_user')      
        response = dataAccess.delete_follow(from_user, to_user)
        if response:
            status.set_status(True)
        else:
            status.set_errorMessage('user not existed')
    return status.get_response()

@app.route("/add_friend") # Two way follows
def add_friend():
   pass

"""
#  ________________________________________
# |Moment Post                             |
# |________________________________________|
"""
@app.route("/momentPost", methods = ['POST'])
def momentPost():
    status = status_response()
    if request.method == 'POST':
        moment_ID = request.form.get('moment_ID')
        attraction_ID = request.form.get('attraction_ID')
        user_ID = request.form.get('user_ID')
        # add moment to database
        response = dataAccess.add_post(moment_ID, attraction_ID, user_ID)
        if response:
            # get all subscribers of this user
            friendList = dataAccess.get_followers(user_ID)
            if friendList:
                # notify the map to propagate the change
                response = notifyMap.momentPropagate(moment_ID, attraction_ID, friendList)
                if response:
                    status.set_status(True)
                else:
                    status.set_errorMessage('fail to notify map')
            else:
                status.set_status(True)
                status.set_errorMessage('no friends')
    return status.get_response()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
