event = {'Records': 
    [
        {
            'messageId': '1c9277fc-2a2e-49d3-8f20-2471886a9850', 
            'receiptHandle': 'AQEBr4GZZyF', 
            'body': '{"LifecycleHookName":"scale-in-lifecycle","AccountId":"990090895087","RequestId":"0af658d8-4d1c-4bf0-9886-16872eb3a892","LifecycleTransition":"autoscaling:EC2_INSTANCE_TERMINATING","AutoScalingGroupName":"EC2ContainerService-api-production-asg","Service":"AWS Auto Scaling","Time":"2018-12-12T11:28:51.086Z","EC2InstanceId":"i-0608a68b58a51e71a","LifecycleActionToken":"888d9b5e-fca7-49ac-a588-ef86a5f4c25b"}', 
            'attributes': {
                'ApproximateReceiveCount': '1', 
                'SentTimestamp': '1544614131120', 
                'SenderId': 'AROAJAX47FVHAZCREOERO:4d130edab0034a0296ffb3c44a6dfe79', 
                'ApproximateFirstReceiveTimestamp': '1544614131127'
                }, 
                'messageAttributes': {}, 
                'md5OfBody': '07936f68dde21a7f4f36677702256c0f', 
                'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-1:990090895087:david-test', 
                'awsRegion': 'ap-southeast-1'
            }
        ]
    }


test_event = {
    "Records":
    [
        {
            "body": {
                "LifecycleHookName": "scale-in-lifecycle", 
                "AutoScalingGroupName": "EC2ContainerService-api-production-asg", 
                "EC2InstanceId": "i-0012362652ecc7ee4"
                }
            }
        ]
    }