# terraform {
#   backend "s3" {
#     bucket = "terraform-test-com"
#     key    = "life-cycle-sqs/terraform.tfstate"
#     region = "ap-southeast-1"
#   }
# }

data "aws_autoscaling_groups" "groups" {
  filter {
    name   = "auto-scaling-group"
    values = ["${var.asg_name}"]
  }
}

resource "aws_autoscaling_lifecycle_hook" "scale-in" {
  name                   = "${var.lifecycle_name}"
  autoscaling_group_name = "${var.asg_name}"
  default_result         = "CONTINUE"
  heartbeat_timeout      = 3600
  lifecycle_transition   = "autoscaling:EC2_INSTANCE_TERMINATING"

  notification_target_arn = "${aws_sqs_queue.lifecycle-scale-in.arn}"
  role_arn                = "arn:aws:iam::${var.account_id}:role/AutoScalingNotificationAccessRole"
}
