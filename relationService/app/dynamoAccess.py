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

## Create table
def create_table(table_name, partitionKeyName, sortingKeyName):
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName = table_name,
        KeySchema=[
            {
                'AttributeName': partitionKeyName,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': sortingKeyName,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partitionKeyName,
                'AttributeType': 'S'
            },
            {
                'AttributeName': sortingKeyName,
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

# add edge
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

# delete edge
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

# batch get
def get_item(table_name, partitionKeyName, partitionKey, sortingKeyName, sortingKey):
    table = dynamodb.Table('friend')
    response = table.get_item(
        Key={
            partitionKeyName: partitionKey,
            sortingKeyName: sortingKey
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    else:
        return False


if __name__ == '__main__':
    pass
