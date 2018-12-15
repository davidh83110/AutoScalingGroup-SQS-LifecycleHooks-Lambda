import unittest
import json
import lambda_function
from ecs import FindClusterName, EcsCluster

class test_handler(unittest.TestCase):
    def test_event(self):
        test_event = {
            "Records":
            [
                {
                    "body": """{
                        "LifecycleHookName": "scale-in-lifecycle", 
                        "AutoScalingGroupName": "EC2ContainerService-api-production-asg", 
                        "EC2InstanceId": "i-0012362652ecc7ee4"
                        }"""
                    }
                ]
            }


        self.assertEqual(lambda_function.event_handler(test_event), (['scale-in-lifecycle', 'EC2ContainerService-api-production-asg', 'i-0012362652ecc7ee4']))


    def test_find_cluster_name(self):
        ## shoplytics-preview instance, test may be fail when this instance no longer exist ### TODO: NEED TO FIX
        to_be_drain_instance_id = 'i-02720f0c3f9be97a1'

        self.assertEqual(FindClusterName(to_be_drain_instance_id).find_cluster_name(), ('shoplytics-preview'))


        

