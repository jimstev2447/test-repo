resource "aws_lambda_function" "etl" {
  function_name = var.lambda_name
  filename      = data.archive_file.lambda.output_path
  role          = aws_iam_role.lambda_role.arn
  handler       = "etl.lambda_handler"
  runtime       = "python3.12"
  timeout       = 10 # default 3 seconds can lead to timeout
  environment {
    variables = {
      STORAGE_BUCKET_NAME : aws_s3_bucket.output_bucket.bucket
    }
  }
  depends_on = [aws_s3_bucket.output_bucket]
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/etl.py"
  output_path = "${path.module}/../function.zip"
}

resource "aws_lambda_permission" "allow_s3" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.etl.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.data_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_lambda_permission" "allow_output" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.etl.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.output_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}
