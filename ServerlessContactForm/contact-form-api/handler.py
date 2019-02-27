import json
import boto3
import os
import time
import uuid
import decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
client = boto3.client('ses')
sender = os.environ['SENDER_EMAIL']
destination = os.environ['DESTINATION_EMAIL']
subject = os.environ['EMAIL_SUBJECT']
configset = os.environ['CONFIG_SET']
charset = 'UTF-8'

def sendMail(event, context):
    print(event)

    try:
        data = event['body']
        content = 'From: ' + data['name'] + '\nEmail: ' + data['email'] + '\nCompany: ' + data['company'] + '\n\nMessage: ' + data['message']
        saveToDynamoDB(data)
        response = sendMailToUser(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:"),
        print(response['MessageId'])
    return "¡Correo Recibido! Estaremos en contacto."

def hello(event, context):
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def saveToDynamoDB(data):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'email': data['email'],
        'company': data['company'],
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return

def sendMailToUser(data, content):
    # Send Email using SES
    return client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                destination,
            ],
        },
        Message={
            'Subject': {
                'Charset': charset,
                'Data': 'Datum Website - Contact Form'
            },
            'Body': {
                'Text': {
                    'Charset': charset,
                    'Data': content
                }
            }
        }
    )

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
