variable "AWS_REGION" {
  default = "ap-southeast-1"
}

variable "asg_name" {}

variable "account_id" {}

variable "lifecycle_name" {
  default = "scale-in-lifecycle"
}

variable "lambda_role_name" {
  default = "LifecycleSQSLambdaRole"
}

variable "asg_notification_role_name" {
  default = "AutoScalingNotificationAccessRole"
}

variable "lambda_function_name" {
  default = "AutoScalingGroup-SQS-LifecycleHooks"
}

variable "sqs_name" {
  default = "asg-lifecycle-scale-in"
}
