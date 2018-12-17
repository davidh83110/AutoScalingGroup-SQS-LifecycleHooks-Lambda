resource "aws_iam_role" "iam_for_lambda" {
  name = "${var.lambda_role_name}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "asg-complete" {
  name        = "ShoplineAsgLifecycleLambda"
  description = "For Lambda complete Lifecycle on Asg"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "autoscaling:CompleteLifecycleAction",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda-attach-asg" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.asg-complete.arn}"
}

resource "aws_iam_policy" "ecs-drain-access" {
  name        = "ShoplineEcsDrainInstance"
  description = "For Lambda drain container instances on ECS"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ecs:UpdateContainerInstancesState",
                "ecs:ListContainerInstances",
                "ecs:DescribeContainerInstances",
                "ecs:DescribeClusters",
                "ecs:ListClusters"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda-attach-ecs" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.ecs-drain-access.arn}"
}

resource "aws_iam_policy" "sqs-lambda-trigger" {
  name        = "ShopSQSLambdaTrigger"
  description = "For Lambda trigger by SQS"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ChangeMessageVisibility",
                "sqs:ReceiveMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda-attach-sqs" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.sqs-lambda-trigger.arn}"
}

resource "aws_iam_role_policy_attachment" "lambda-attach-execute" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}
