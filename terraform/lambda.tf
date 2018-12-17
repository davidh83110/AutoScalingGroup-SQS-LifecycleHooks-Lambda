resource "aws_lambda_function" "test_lambda" {
  filename         = "lambda_function_payload.zip"
  function_name    = "lambda_function_name"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "exports.test"
  source_code_hash = "${base64sha256(file("../lambda_function_payload.zip"))}"
  runtime          = "nodejs8.10"

  environment {
    variables = {
      foo = "bar"
    }
  }
}
