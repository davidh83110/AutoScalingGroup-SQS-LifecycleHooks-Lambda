data "template_file" "sqs-policy" {
  template = "${file("sqs-policy.json")}"

  vars {
    account_id     = "${var.account_id}"
    lifecycle_name = "${var.lifecycle_name}"
    asg_arn        = "${element(data.aws_autoscaling_groups.groups.arns, 0)}"
    region         = "${var.AWS_REGION}"
  }
}

resource "aws_sqs_queue" "lifecycle-scale-in" {
  name                      = "asg-lifecycle-scale-in"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  policy                    = "${data.template_file.sqs-policy.rendered}"
}
