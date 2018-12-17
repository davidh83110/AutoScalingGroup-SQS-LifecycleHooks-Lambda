resource "aws_lambda_function" "lifecycle-sqs" {
  filename         = "lambda_function_payload.zip"
  function_name    = "AutoScalingGroup-SQS-LifecycleHooks"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = "${base64sha256(file("../lambda_function_payload.zip"))}"
  runtime          = "python3.6"
}
