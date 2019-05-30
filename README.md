# AutoScalingGroup Lifecycle Hooks with Lambda and SQS

[![Build Status](https://travis-ci.org/davidh83110/AutoScalingGroup-SQS-LifecycleHooks-Lambda.svg?branch=master)](https://travis-ci.org/davidh83110/AutoScalingGroup-SQS-LifecycleHooks-Lambda)

### Environment
- Python 3.6
- AWS Lambda
- AWS SQS
- AWS EC2 AutoScalingGroup Lifecycle Hooks
- AWS IAM Role
- boto3
- unittest
- Pipelines only update Lambda code, won't apply any changes on terrform scripts
---

### AWS
#### SQS
- Create a SQS and attach policy which allow all asg resources access

```
{
    "Version": "2012-10-17",
    "Id": "arn:aws:sqs:${region}:${account_id}:${lifecycle_name}/SQSDefaultPolicy",
    "Statement": [
        {
        "Sid": "Sid1544608181745",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
        },
        "Action": "SQS:SendMessage",
        "Resource": "arn:aws:sqs:${region}:${account_id}:${lifecycle_name}",
        "Condition": {
            "ArnEquals": {
            "aws:SourceArn": "arn:aws:autoscaling:${region}:${account_id}:autoScalingGroup:*"
            }
        }
        }
    ]
}
```

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

### How to add a new ASG to use Lifecycle with this repo ?
- add a `aws_autoscaling_groups` data fetch on asg.tf and create a variable with asg name on var.tf
- add a `aws_autoscaling_lifecycle_hook` on asg.tf with asg name we wanna apply
- going to `terraform init -reconfigure` and `terraforn apply`

---

### Flowchart


![text](https://github.com/davidh83110/AutoScalingGroup-SQS-LifecycleHooks-Lambda/blob/master/flowchart.png?raw=true)
