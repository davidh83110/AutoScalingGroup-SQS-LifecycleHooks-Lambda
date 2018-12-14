import boto3

class EcsCluster(object):

    def __init__(self, cluster_name):
        self.cluster_name = cluster_name
        self.ecs = boto3.client('ecs')


    def get_node(self, cluster_name, instancd_id):
        ecs_res = ecs.list_container_instances(
            cluster=cluster_name
        )
        instance_arns = ecs_res['containerInstanceArns']

        ecs_describe = ecs.describe_container_instances(
            cluster=cluster_name,
            containerInstances=instance_arns
        )

        for node in ecs_describe['containerInstances']:
            if node['ec2InstanceId'] == instancd_id:
                ### draining instance ###

