variable "AWS_REGION" {
  default = "ap-southeast-1"
}

variable "asg_name" {
  default = "EC2ContainerService-api-production-asg"
}

variable "account_id" {
  default = "990090895087"
}

variable "lifecycle_name" {
  default = "scale-in-lifecycle"
}

variable "lambda_role_name" {
  default = "LifecycleSQSLambdaRole"
}
