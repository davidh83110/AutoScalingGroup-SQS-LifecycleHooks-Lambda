import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class FindClusterName(object):
    
    def __init__(self, to_be_drain_instance_id):
        self.ecs = boto3.client('ecs')
        self.instance_id = to_be_drain_instance_id
        

    def find_cluster_name(self):
        all_clusters = self.ecs.list_clusters()['clusterArns']

        combined_cluster_instance_list = []

        for cluster_ecs in all_clusters:
            ecs_cluster_name = cluster_ecs.split('/')[1]
            
            list_all_instances = self.ecs.list_container_instances(cluster=cluster_ecs.split('/')[1])
            all_instance_arns = list_all_instances['containerInstanceArns']
            
            for arn in all_instance_arns:
            
                if arn == []:
                    pass
                else:
                    describe_instance = self.ecs.describe_container_instances(cluster=ecs_cluster_name,
                                                                containerInstances=[arn])
                    instance_id_keys = describe_instance['containerInstances'][0]['ec2InstanceId']
                    combined_cluster_instance_list.append(ecs_cluster_name + '///' + instance_id_keys)

        for cluster_instance in combined_cluster_instance_list:
            all_cluster_name = cluster_instance.split('///')[0]
            all_instance_id = cluster_instance.split('///')[1]

            if all_instance_id == self.instance_id:
                print('match', str(all_cluster_name))
                cluster_name = all_cluster_name
                logger.info('cluster name: ' + cluster_name)

                return cluster_name

    

class EcsCluster(object):

    def __init__(self, to_be_drain_instance_id, cluster_name):
        self.cluster_name = cluster_name
        self.ecs = boto3.client('ecs')
        self.instance_id = to_be_drain_instance_id



    def describe_container_instance(self, instance_arns):
        ecs_describe = self.ecs.describe_container_instances(
            cluster=self.cluster_name,
            containerInstances=[instance_arns]
        )

        return ecs_describe


    def drain_container_instance(self, container_instance_arn):
        update_response = self.ecs.update_container_instances_state(
            cluster=self.cluster_name,
            containerInstances=[container_instance_arn],
            status='DRAINING'
        )
        logger.info('draining container instance...' + str(update_response))


    def ecs_handle(self):
        print(self.cluster_name)
        ecs_res = self.ecs.list_container_instances(
            cluster=self.cluster_name
        )
        instance_arns = ecs_res['containerInstanceArns']
        
        for arn in instance_arns:
            ecs_describe = self.describe_container_instance(arn)

            for node in ecs_describe['containerInstances']:
            
                if node['ec2InstanceId'] == self.instance_id:
                    to_be_drain_instance_arn = node['containerInstanceArn']

                    ### draining instance ###
                    self.drain_container_instance(to_be_drain_instance_arn)

                    ### checking drain status ###
                    if self.check_container_instance(to_be_drain_instance_arn):
                        logger.info(self.instance_id + ' - drain container instance done')
                    else:
                        logger.error(self.instance_id + ' - draining container instance failed')



    def check_container_instance(self, to_be_drain_instance_arn):

        drining_instance_task_running_count = self.describe_container_instance(to_be_drain_instance_arn)['runningTasksCount']

        while drining_instance_task_running_count == 0:
            return True
        


