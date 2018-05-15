"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file sends http request to mapService to update maps for users

"""
import requests
from endpoints import mapService_ENDPOINT

# when a new moment is posted
def momentPropagate(moment_ID, attraction_ID, friendList):
    
    url = mapService_ENDPOINT + '/momentPropagate'

    data = {
        'moment_ID': moment_ID,
        'attraction_ID': attraction_ID,
        'friendList': friendList
    }

    try:
        response = requests.post(url, data = data)
        if response['status']:
            return True
        else:
            return False
    except:
        return False

# when a new follow is added
def followPropagate(momentDictList, user_ID):
    url = mapService_ENDPOINT + '/followPropagate'

    data = {
        'momentDictList': momentDictList,
        'user_ID': user_ID
    }
    
    try:
        response = requests.post(url, data = data)
        if response['status']:
            return True
        else:
            return False
    except:
        return False

