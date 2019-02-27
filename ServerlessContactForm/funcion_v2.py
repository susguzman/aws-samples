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

def sendMail(event, context):
    print(event)

    try:
        content = 'From: ' + event['name'] + '\nEmail: ' + event['email'] + '\n\nMessage: ' + event['message']
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
