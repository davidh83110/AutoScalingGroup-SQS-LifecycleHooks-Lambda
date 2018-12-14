import json
import boto3
import ecs
import logging

logger=None
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
    logger.info(f'Lifecycle Hooks Name: {lifecyclehook_name}')

    asg_name = event_body['AutoScalingGroupName']
    logger.info(f'ASG Name: {asg_name}')

    to_be_drain_instance_id = event_body['EC2InstanceId']
    logger.info(f'To be drain Instance ID: {to_be_drain_instance_id}')

    lifecycle_argument_list = [lifecyclehook_name, asg_name, to_be_drain_instance_id]
    logger.info('starting draining container instance.....')

    ecs.EcsCluster.ecs_handle()

    complete_lifecycle_action(lifecycle_argument_list)
    
    return {
        'statusCode': 200,
        'body': json.dumps('done')
    }
