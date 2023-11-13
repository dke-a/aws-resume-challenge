resource "aws_lambda_function" "lambda_function" {
  function_name = var.function_name
  handler       = var.handler
  role          = var.iam_role_arn
  runtime       = var.runtime

  filename = "${path.module}/lambda_function/lambda_function.zip"

  source_code_hash = filebase64sha256("${path.module}/lambda_function/lambda_function.zip")

  #   environment {
  #     variables = var.environment_variables
  #   }
}

# Additional resources like IAM roles, policies, and event triggers can be defined here
