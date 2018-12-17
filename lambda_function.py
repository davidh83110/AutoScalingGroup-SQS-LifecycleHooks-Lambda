import json
import boto3
from ecs import EcsCluster, FindClusterName
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

asg = boto3.client('autoscaling')

def check_response(response):
    return int(response['ResponseMetadata']['HTTPStatusCode']) == 200

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

def event_handler(event):
    try:
        event_body = json.loads(event['Records'][0]['body'])

        lifecyclehook_name = event_body['LifecycleHookName']
        logger.info('Lifecycle Hooks Name: ' + lifecyclehook_name)

        asg_name = event_body['AutoScalingGroupName']
        logger.info('ASG Name: ' + asg_name)

        to_be_drain_instance_id = event_body['EC2InstanceId']
        logger.info('To be drain Instance ID: ' + to_be_drain_instance_id)

        lifecycle_argument_list = [lifecyclehook_name, asg_name, to_be_drain_instance_id]

        return lifecycle_argument_list

    except Exception as e:
        logger.info(event)
        logger.error('parse lifecycle event argument error %s' % (e))
        return None

def lambda_handler(event, context):
    
    lifecycle_argument_list = event_handler(event)
    to_be_drain_instance_id = lifecycle_argument_list[2]

    logger.info('starting draining container instance.....')

    ## find cluster name
    cluster_name = FindClusterName(to_be_drain_instance_id).find_cluster_name()
    if cluster_name == []:
        logger.error('cluster name is null')

    ## start draining
    EcsCluster(to_be_drain_instance_id, cluster_name).ecs_handle()
    ## start completing lifecycle 
    complete_lifecycle_action(lifecycle_argument_list)

    logger.info('instance drained and lifecycle completed, instance will be terminate now.')

    return {
        'statusCode': 200,
        'body': json.dumps('done')
    }
