resource "aws_lambda_function" "lifecycle-sqs" {
  filename         = "lambda_function_payload.zip"
  function_name    = "${var.lambda_function_name}"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = "${base64sha256(file("../lambda_function_payload.zip"))}"
  runtime          = "python3.6"
}

resource "aws_lambda_event_source_mapping" "sqs-lambda" {
  event_source_arn = "${aws_sqs_queue.lifecycle-scale-in.arn}"
  function_name    = "${aws_lambda_function.lifecycle-sqs.function_name}"
  batch_size       = 1
}
