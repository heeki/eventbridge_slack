import boto3
import json

# initialization
session = boto3.session.Session()
client = session.client('events')

def handler(event, context):
    print(json.dumps(event))
    return event
