import json
import boto3
import os
import time
import uuid
import decimal
from botocore.exceptions import ClientError

ses = boto3.client('ses')
sender = os.environ['SENDER_EMAIL']
destination = os.environ['DESTINATION_EMAIL']
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']

def sendMail(event, context):
    print(event)

    try:
        content = 'From: ' + event['name'] + '\nEmail: ' + event['email'] + '\n\nMessage: ' + event['message']
        saveToDynamoDB(event)
        response = sendMailToUser(event, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:"),
        print(response['MessageId'])
    return "Email sent!"

def sendMailToUser(data, content):
    # Send Email using SES
    return ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                destination,
            ],
        },
        Message={
            'Subject': {
                'Data': 'Contacto: ' + data['subject']
            },
            'Body': {
                'Text': {
                    'Data': content
                }
            }
        }
    )

def saveToDynamoDB(data):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(table_name)
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'email': data['email'],
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    return table.put_item(Item=item)
