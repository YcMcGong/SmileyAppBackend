"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides application specific data-access functions.

"""
# table names
FRIEND_TABLE = 'relationService_Friend'
MOMENT_TABLE = 'relationService_Moment'

from datetime import datetime
import dynamoAccess
import uuid
import hmac

# table names
EMAIL_LOOKUP_TABLE = 'authSerive_Email_Lookup'
EXP_ID_LOOKUP_TABLE = 'authSerive_Exp_ID_Lookup'
USER_TABLE = 'authSerive_User_Table'

# helpers
def hash_password(secret, password):
    return hmac.new(secret.encode('utf-8'), password.encode('utf-8')).hexdigest()

# register a new user
def user_sign_up(email, password, firstName, lastName, username, **kwargs):
    token = uuid.uuid4() # get a random uuid
    user_ID = str(uuid.uuid5(token, username)) # generate a user_ID using username
    password_hashed = hash_password(user_ID, password)
    response = dynamoAccess.add(USER_TABLE, 'user_ID', user_ID, 'dataType', 'basic',
        firstName = firstName, lastName = lastName, username = username, **kwargs)
    response = dynamoAccess.add(USER_TABLE, 'user_ID', user_ID, 'dataType', 'credential', password = password_hashed)
    response = dynamoAccess.add(EMAIL_LOOKUP_TABLE, 'email', email, user_ID = user_ID)
    response = dynamoAccess.add(EXP_ID_LOOKUP_TABLE, 'exp_ID', username, user_ID = user_ID)
    return response

# add or change user data
def user_log(user_ID, dataType, **kwargs):
    response = dynamoAccess.add(USER_TABLE, 'user_ID', user_ID, 'dataType', dataType, **kwargs)
    return response

# get user data
def user_get(user_ID, dataType = None):
    if dataType:
        response = dynamoAccess.get_item(USER_TABLE, 'user_ID', user_ID, 'dataType', dataType)
    else:
        response = dynamoAccess.query(USER_TABLE, 'user_ID', user_ID)
    return response

# get user basic info
def user_get_basic(user_ID):
    return user_get(user_ID, dataType = 'basic')

# get user credential
def user_get_credential(user_ID):
    return user_get(user_ID, dataType='credential')

# delete user
def user_delete(user_ID):
    response = user_get(user_ID)
    for i in response:
        dataType = i['dataType']
        dynamoAccess.delete(USER_TABLE, 'user_ID', user_ID, 'dataType', dataType)

# email look up
def lookup_email(email):
    response = dynamoAccess.get_item(EMAIL_LOOKUP_TABLE, 'email', email)
    return response['user_ID']

#  username look up
def lookup_username(username):
    response = dynamoAccess.get_item(EXP_ID_LOOKUP_TABLE, 'exp_ID', username)
    return response['user_ID']

# user authenticate
def user_authenticate(user_ID = None, email = None, username = None, password = None):
    if password:
        if user_ID:
            response = user_get_credential(user_ID)
            if hash_password(user_ID, password) == response['password']:
                return True
            else:
                return False

        elif email:
            user_ID = lookup_email(email)
            response = user_get_credential(user_ID)
            if hash_password(user_ID, password) == response['password']:
                return True
            else:
                return False

        elif username:
            user_ID = lookup_username(username)
            response = user_get_credential(user_ID)
            if hash_password(user_ID, password) == response['password']:
                return True
            else:
                return False

    return False
            

# unit test
if __name__ == '__main__':
    # print(user_sign_up('test@gmail.com', '123', 'mc', 'king', 'user_01', job = 'student'))
    # print(user_log(user_ID = '773e4629-1049-561b-b35b-d58b0aaf8710', dataType = 'work', salary = 1000, job = 'teacher'))
    print(user_authenticate(username = 'user_01', password='123'))
    # print(lookup_email('test@gmail.com'))
