import boto3
import logging

logger=None

class EcsCluster(object):

    def __init__(self, cluster_name, to_be_drain_instance_id):
        self.cluster_name = cluster_name
        self.ecs = boto3.client('ecs')
        self.instance_id = to_be_drain_instance_id


    def describe_container_instance(self, instance_arns):
        ecs_describe = self.ecs.describe_container_instances(
            cluster=self.cluster_name,
            containerInstances=instance_arns
        )

        return ecs_describe


    def drain_container_instance(self, container_instance_arn):
        update_response = self.ecs.update_container_instances_state(
            cluster=self.cluster_name,
            containerInstances=container_instance_arn,
            status='DRAINING'
        )
        logger.info(f'draining container instance...{update_response}')


    def ecs_handle(self, cluster_name, instancd_id):
        ecs_res = self.ecs.list_container_instances(
            cluster=self.cluster_name
        )
        instance_arns = ecs_res['containerInstanceArns']

        ecs_describe = self.describe_container_instance(instance_arns)

        for node in ecs_describe['containerInstances']:
            if node['ec2InstanceId'] == self.instance_id:
                to_be_drain_instance_arn = node['containerInstanceArn']

                ### draining instance ###
                self.drain_container_instance(to_be_drain_instance_arn)

                ### checking drain status ###
                if self.check_container_instance(to_be_drain_instance_arn):
                    logger.info(f'{self.instance_id} - drain container instance done')
                else:
                    logger.error(f'{self.instance_id} - draining container instance failed')
            else:
                logger.error(f'{node["ec2InstanceId"]} != {self.instance_id} - intance id not found in cluster instance list')


    def check_container_instance(self, to_be_drain_instance_arn):

        drining_instance_task_running_count = self.describe_container_instance(to_be_drain_instance_arn)['runningTasksCount']

        while drining_instance_task_running_count == 0:
            return True
