"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides low-level DynamoDB interfaces.

"""
# Imports
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
try: 
    # provide config.py for local testing
    # if config.py not present, use IAM role instead
    from config import aws_access_key_id, aws_secret_access_key
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,)
except:
    dynamodb = boto3.resource('dynamodb',region_name='us-west-1')


# add data
def add(table_name, partitionKeyName, partitionKey, sortingKeyName, sortingKey, **kwargs): 
    
    table = dynamodb.Table(table_name)
    data = {partitionKeyName: partitionKey, sortingKeyName: sortingKey}
    for key in kwargs:
        data[key] = kwargs[key]
    response = table.put_item(
        Item = data
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

# add data for a table with no sorting key
def add_partition_only(table_name, partitionKeyName, partitionKey, **kwargs): 
    
    table = dynamodb.Table(table_name)
    data = {partitionKeyName: partitionKey}
    for key in kwargs:
        data[key] = kwargs[key]
    response = table.put_item(
        Item = data
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

# batch add
def batch_add_to_multiple_partitions(table_name, partitionKeyName, partitionKeyList, sortingKeyName, sortingKey, **kwargs):

    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for partitionKey in partitionKeyList:
            data = {partitionKeyName: partitionKey, sortingKeyName: sortingKey}
            for key in kwargs:
                data[key] = kwargs[key]
            batch.put_item(
                Item = data
            )
    return True

# batch add partition only
def batch_add_partition_only(table_name, partitionKeyName, partitionKeyList, **kwargs):
    
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for partitionKey in partitionKeyList:
            data = {partitionKeyName: partitionKey}
            for key in kwargs:
                data[key] = kwargs[key]
            batch.put_item(
                Item = data
            )
    return True

# delete data
def delete(table_name, partitionKeyName, partitionKey, sortingKeyName, sortingKey):
    
    table = dynamodb.Table(table_name)

    response = table.delete_item(
        Key={
            partitionKeyName: partitionKey,
            sortingKeyName: sortingKey,
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

# delete data for a table with no sorting key
def delete_partition_only(table_name, partitionKeyName, partitionKey):
    
    table = dynamodb.Table(table_name)

    response = table.delete_item(
        Key={
            partitionKeyName: partitionKey
            }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

# query
def query(table_name, partitionKeyName, partitionKey):
    table = dynamodb.Table(table_name)
    # query
    response = table.query(
        KeyConditionExpression=Key(partitionKeyName).eq(partitionKey)
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    else:
        return False

# get item
def get_item(table_name, partitionKeyName, partitionKey, sortingKeyName, sortingKey):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            partitionKeyName: partitionKey,
            sortingKeyName: sortingKey
        }
    )
    try:
        return response['Item']
    except:
        return False

# get item with partition only
def get_item_partition_only(table_name, partitionKeyName, partitionKey, attribute):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            partitionKeyName: partitionKey
        }
    )
    try:
        return response['Item'][attribute]
    except:
        return False

# update
def update(table_name, partitionKeyName, partitionKey, sortingKeyName, sortingKey, data):
    table = dynamodb.Table(table_name)
    result = table.update_item(
        Key={
            partitionKeyName: partitionKey,
            sortingKeyName: sortingKey
        },
        UpdateExpression="SET data = list_append(:i, data)",
        ExpressionAttributeValues={
            ':i': [data],
        },
        ReturnValues="UPDATED_NEW"
    )

# update for partition key only
def update_for_partition_only(table_name, partitionKeyName, partitionKey, data):
    table = dynamodb.Table(table_name)
    result = table.update_item(
        Key={
            partitionKeyName: partitionKey,
        },
        UpdateExpression="SET data = list_append(:i, data)",
        ExpressionAttributeValues={
            ':i': [data],
        },
        ReturnValues="UPDATED_NEW"
    )

# ///////////////////////////
# mapService specific methods
# ///////////////////////////
def batch_add_one_to_many(table_name, partitionKeyName, partitionKeyList, 
    sortingKeyName, sortingKey, partitionKeySuffix = '', **kwargs):

    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for partitionKey in partitionKeyList:
            data = {partitionKeyName: partitionKey + partitionKeySuffix, sortingKeyName: sortingKey}
            for key in kwargs:
                data[key] = kwargs[key]
            batch.put_item(
                Item = data
            )
    return True

def batch_add_many_to_one(table_name, partitionKeyName, partitionKey, 
    sortingKeyName, sortingKeyList, partitionKeyPrefix = '', **kwargs):

    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for sortingKey in sortingKeyList:
            data = {partitionKeyName: partitionKeyPrefix + partitionKey, sortingKeyName: sortingKey}
            for key in kwargs:
                data[key] = kwargs[key]
            batch.put_item(
                Item = data
            )
    return True

from datetime import datetime
if __name__ == '__main__':
    # test
    # for i in range(100):
        # add('mapService_User_Attraction', 'user_ID', '1', 'attraction_ID', str(datetime.now()))
    # print(query('mapService_User_Attraction', 'user_ID', '1'))
    pass
