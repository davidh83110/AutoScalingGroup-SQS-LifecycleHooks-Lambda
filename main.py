import json
import boto3

asg = boto3.client('autoscaling')

def complete_lifecycle_action(lifecyclehook_name, to_be_drain_instance_id):
    response = asg.complete_lifecycle_action(
        LifecycleHookName=lifecyclehook_name,
        AutoScalingGroupName='string',
        LifecycleActionResult='string',
        InstanceId=to_be_drain_instance_id
    )

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    
    event = {'Records': [{'messageId': '1c9277fc-2a2e-49d3-8f20-2471886a9850', 'receiptHandle': 'AQEBr4GZZyFuM20C7HgImauQcNYMYdIev39mkhx1m3gbydnYsADiwcoiK05iTMXUb/uBbbURarx411dnzly3CpRyu9FYRSy1A/YdYkoJSRTHfzcJA62I19oo0qOTGt9odPbWjfztTJyYCLLJ1MLMr5IUJqqUDW8tyX3gvNJwzciW7nq4IU+3zOACLZGY1qrWkUdNp7M/F1Vg4bC8A8BPGIpQuYF7bDN8a0Q4wDPAf6E6s9apKVQ/EVxKZnpsPW/57mUPJtPEp3/H+1AptPtm2jcZUMScTyMKWbWouFAlXnCwdLd9kwU7+7riRsay46++Y+kwj8PuFTbu6vH3n2fJs8ZM1IArwocNHz04D54pjWVU23ekZPu1G8ajIpPCHU/Jk/UxeRSDKf60edJb1zMQYFpaEQ==', 'body': '{"LifecycleHookName":"scale-in-lifecycle","AccountId":"990090895087","RequestId":"0af658d8-4d1c-4bf0-9886-16872eb3a892","LifecycleTransition":"autoscaling:EC2_INSTANCE_TERMINATING","AutoScalingGroupName":"EC2ContainerService-api-production-asg","Service":"AWS Auto Scaling","Time":"2018-12-12T11:28:51.086Z","EC2InstanceId":"i-0608a68b58a51e71a","LifecycleActionToken":"888d9b5e-fca7-49ac-a588-ef86a5f4c25b"}', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1544614131120', 'SenderId': 'AROAJAX47FVHAZCREOERO:4d130edab0034a0296ffb3c44a6dfe79', 'ApproximateFirstReceiveTimestamp': '1544614131127'}, 'messageAttributes': {}, 'md5OfBody': '07936f68dde21a7f4f36677702256c0f', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-1:990090895087:david-test', 'awsRegion': 'ap-southeast-1'}]}
    event_body = json.loads(event['Records'][0]['body'])

    lifecyclehook_name = event_body['LifecycleHookName']
    print(lifecyclehook_name)
    
    to_be_drain_instance_id = event_body['EC2InstanceId']
    print(to_be_drain_instance_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
