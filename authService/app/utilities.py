"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides useful utility classes.

"""
from flask import jsonify

class status_response():

    def __init__(self):
        self.data = {
            'status': False,
            'errorMessage': []
        }

    def set_status(self, isSuccess):
        self.data['status'] = isSuccess

    def set_errorMessage(self, message):
        self.data['errorMessage'] = self.data['errorMessage'].push(message)

    def attach_data(self, name, data, isSuccess = False):
        self.data[name] = data
        if isSuccess:
            self.data['status'] = True

    def get_response(self):
        return jsonify(self.data)