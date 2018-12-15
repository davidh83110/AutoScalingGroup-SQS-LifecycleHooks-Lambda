import unittest
import lambda_function

class test_handler(unittest.TestCase):
    def test_event(self):
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


        self.assertEqual(lambda_function.event_handler(test_event), (['EC2ContainerService-api-production-asg', 'api-production', 'i-0012362652ecc7ee4']))


        

