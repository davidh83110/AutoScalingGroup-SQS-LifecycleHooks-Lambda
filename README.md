## AutoScalingGroup Lifecycle Hooks with Lambda and SQS

### Environment
- Python 3.6
- AWS Lambda
- AWS SQS
- AWS EC2 AutoScalingGroup Lifecycle Hooks
- AWS IAM Role
- boto3
- unittest
 
---

### AWS
#### SQS
- Create a SQS
#### EC2 AutoScalingGroup Lifecycle Hooks
- Create Lifecycle Hooks with AWS cli (must be) to invoke SQS
```
aws autoscaling put-lifecycle-hook --lifecycle-hook-name scale-in-lifecycle \
 --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING \
 --auto-scaling-group-name EC2ContainerService-api-production-asg \
 --notification-target-arn \
 arn:aws:sns:ap-southeast-1:990090895087:david-test-asg-lifecycle \
 --role-arn arn:aws:iam::990090895087:role/AutoScalingNotificationAccessRole
```

---

### Flowchart


![text](https://github.com/davidh83110/AutoScalingGroup-SQS-LifecycleHooks-Lambda/blob/master/flowchart.png?raw=true)