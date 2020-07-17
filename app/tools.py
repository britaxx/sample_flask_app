import boto3
import os, io
import json
from flask import current_app
import base64, uuid
from .utils import *

dynamodb_client = boto3.client('dynamodb', region_name=current_app.config['AWS_REGION'])

s3_client = boto3.client("s3", region_name=current_app.config['AWS_REGION'])

def scan_table(dynamo_client, *, TableName, **kwargs):
    """
    Generates all the items in a DynamoDB table.

    :param dynamo_client: A boto3 client for DynamoDB.
    :param TableName: The name of the table to scan.

    Other keyword arguments will be passed directly to the Scan operation.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    """
    paginator = dynamodb_client.get_paginator("scan")

    for page in paginator.paginate(TableName=TableName, **kwargs):
        yield from page["Items"]


def get_items(TableName, key, **kwargs):
    response= dynamodb_client.query(
        TableName=TableName,
        KeyConditionExpression='id = :id',
        ExpressionAttributeValues={
            ':id': {'S': key}
        },
        **kwargs
    )
    last_value = response.get('Items')
    if len(last_value) == 0:
        return {}
    
    last_value = last_value.pop()
    return last_value

def get_photos(bucket_name):
    """
    Get Photos from DynamoDB
    """
    data = []
    print ("Bucket {}".format(bucket_name))
    bucket_items = s3_client.list_objects(Bucket=bucket_name)
    # print ("Photos from s3 {}".format(bucket_items.get('Contents', {})))
    
    for item in bucket_items.get('Contents', []):
        dynamo_item = get_items(TableName=current_app.config['DYNAMO_TABLE_NAME'], key=item['Key'])
        all_rekognitions = [x.get('M', {}) for x in dynamo_item.get('Labels', {}).get('L', {})]
        all_labels = [list(x.keys()) for x in all_rekognitions]
        # print (item)
        data.append({
            'signed_url': s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': item['Key']}),
            'labels': all_labels[0:5],
            'created_datetime': item['LastModified'].strftime("%d/%m/%Y, %H:%M:%S")
        })
    return data


def upload_file_to_s3(file, bucket_name, acl="private"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        image_bytes = file
        key = file.filename
        s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=image_bytes,
                ContentType=file.content_type
            )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return True
