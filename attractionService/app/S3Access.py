"""
____________________________________________________
 Copyright 2018 Bangtian Zhou
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides S3 access capability.

"""
import boto3
from endpoints import REGION, PROFILE_PIC_BUCKET

try:
    from config import aws_access_key_id, aws_secret_access_key
    s3 = boto3.client(
        's3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
        region_name=REGION
    )

except:
    s3 = boto3.client('s3')

def generate_presigned_upload_url(bucket_name, key, timeout = 3600, method = 'PUT'):
    try:
        url = s3.generate_presigned_url('put_object', 
            Params={'Bucket':bucket_name, 'Key':key}, 
            ExpiresIn=timeout, 
            HttpMethod=method)
        return url
    except:
        return False

def get_url(bucket_name, key, timeout = 3600, method = 'GET'):
    try:
        url = s3.generate_presigned_url('get_object', 
            Params={'Bucket':bucket_name, 'Key':key}, 
            ExpiresIn=timeout, 
            HttpMethod=method)
        return url
    except:
        return False

if __name__ == '__main__':
    print(generate_presigned_upload_url(PROFILE_PIC_BUCKET, 'test10.jpg'))
    print(get_url(PROFILE_PIC_BUCKET, 'test10.jpg'))