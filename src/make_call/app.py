import boto3
import json
import os

client = boto3.client('connect', region_name=os.environ['connect_region'])


def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        sns_message = record['Sns']['Message']
        print(sns_message)
        content = json.loads(sns_message)['detail']['content']

        if not 'phone_e164' in content:
            print('necessary fields are missed')
            return

        print(content)

        client.start_outbound_voice_contact(
            DestinationPhoneNumber=content['phone_e164'],
            InstanceId=os.environ['connect_instance_id'],
            ContactFlowId=os.environ['connect_contact_flow_id'],
            SourcePhoneNumber=os.environ['connect_source_phone_number'],
            Attributes=content
        )
