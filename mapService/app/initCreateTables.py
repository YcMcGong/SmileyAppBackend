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
from config import aws_access_key_id, aws_secret_access_key

# table names
USER_MAP_TABLE = 'mapService_User_Map'
USER_ATTRACTION_TABLE = 'mapService_User_Attraction'

# Get the service resource.

dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,)

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

def create_table_partition_only(table_name, partitionKeyName):
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName = table_name,
        KeySchema=[
            {
                'AttributeName': partitionKeyName,
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partitionKeyName,
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
if __name__ == '__main__':
    create_table(USER_ATTRACTION_TABLE, 'u_a_ID', 'time')
    create_table(USER_MAP_TABLE, 'user_ID', 'time')