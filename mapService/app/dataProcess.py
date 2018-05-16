"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides application specific data-access functions.

"""
# table names
USER_MAP_TABLE = 'mapService_User_Map'
USER_ATTRACTION_TABLE = 'mapService_User_Attraction'

import dynamoAccess

# momentPopagate helper
def rankInsert(data, dataList):
    return dataList

# propagate a moment to list of users
def momentPopagate(moment_ID, attraction_ID, friendList):
    data = [0, 2, 3 ]  # need to make a call to attraction service
    time = 0
    sortingKeySuffix = '-' + 'attraction_ID'
    # update user moments for attraction
    dynamoAccess.batch_add_one_to_many(USER_ATTRACTION_TABLE, 'u_a_ID', friendList, 
        'time', time, partitionKeySuffix=sortingKeySuffix)
    # update user attraction map
    dynamoAccess.batch_add_one_to_many(USER_MAP_TABLE, 'user_ID', friendList, 'time', time, attraction_ID = attraction_ID)
        
def followPropagate(momentList, user_ID):
    mementList = momentList # should make a call to attractionService to get a list of 'moment_ID, attraction_ID, time, details'
    # update user moments for attraction




""" OLD CODE
/////////////////////////////////////
# propagate a moment to list of users
def momentPopagate(moment_ID, attraction_ID, friendList):
    data = [0, 2, 3 ]  # need to make a call to attraction service
    for user_ID in friendList:
        # update attraction
        try:
            dynamoAccess.update(USER_ATTRACTION_TABLE, 'user_ID', user_ID, 'attraction_ID', attraction_ID, data = data)
        except:
            dynamoAccess.add(USER_ATTRACTION_TABLE, 'user_ID', user_ID, 'attraction_ID', attraction_ID, data = data)
        # update map
        try:
            dataList = dynamoAccess.get_item_partition_only(USER_MAP_TABLE, 'user_ID', user_ID, 'data')
            dataList = rankInsert(data, dataList)
        except:
            dataList = [data]
            dynamoAccess.add_partition_only(USER_MAP_TABLE, 'user_ID', user_ID, data = dataList)

def followPropagate(momentList, user_ID):
    for post in momentList:
        moment_ID = post['moment_ID']
        attraction_ID = post['attraction_ID']
        time = post['time']
        data = [moment_ID, attraction_ID, time]
        try:
            dynamoAccess.update(USER_ATTRACTION_TABLE, 'user_ID', user_ID, 'attraction_ID', attraction_ID, data = data)
        except:
            dynamoAccess.add(USER_ATTRACTION_TABLE, 'user_ID', user_ID, 'attraction_ID', attraction_ID, data = data)
        # update map
        try:
            dataList = dynamoAccess.get_item_partition_only(USER_MAP_TABLE, 'user_ID', user_ID, 'data')
            dataList = rankInsert(data, dataList)
        except:
            dataList = [data]
            dynamoAccess.add_partition_only(USER_MAP_TABLE, 'user_ID', user_ID, data = dataList)
"""