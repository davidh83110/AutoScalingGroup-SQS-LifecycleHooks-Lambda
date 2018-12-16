resource "aws_sqs_queue" "lifecycle-scale-in" {
  name                      = "asg-lifecycle-scale-in"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  policy                    = "${file("sqs-policy.json")}"
}
