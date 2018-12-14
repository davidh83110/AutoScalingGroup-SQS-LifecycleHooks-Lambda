import json
import boto3
from ecs import EcsCluster
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

asg = boto3.client('autoscaling')

def check_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def complete_lifecycle_action(lifecycle_argument_list):
    response = asg.complete_lifecycle_action(
        LifecycleHookName=lifecycle_argument_list[0],
        AutoScalingGroupName=lifecycle_argument_list[1],
        LifecycleActionResult='CONTINUE',
        InstanceId=lifecycle_argument_list[2]
    )

    if check_response(response):
        logger.info('Lifecycle hook continue correctly')
    else:
        logger.error('lifecycle hook could not be continue')

    return None

def lambda_handler(event, context):
    
    event_body = json.loads(event['Records'][0]['body'])

    lifecyclehook_name = event_body['LifecycleHookName']
    logger.info('Lifecycle Hooks Name: ' + lifecyclehook_name)

    asg_name = event_body['AutoScalingGroupName']
    logger.info('ASG Name: ' + asg_name)

    to_be_drain_instance_id = event_body['EC2InstanceId']
    logger.info('To be drain Instance ID: ' + to_be_drain_instance_id)

    lifecycle_argument_list = [lifecyclehook_name, asg_name, to_be_drain_instance_id]
    logger.info('starting draining container instance.....')

    ## start draining
    EcsCluster(to_be_drain_instance_id).ecs_handle()

    ## start completing lifecycle 
    complete_lifecycle_action(lifecycle_argument_list)

    logger.info('instance drained and lifecycle completed, instance will be terminate now.')
    
    return {
        'statusCode': 200,
        'body': json.dumps('done')
    }
