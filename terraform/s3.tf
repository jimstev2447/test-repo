resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "nc-de-code-"
}

resource "aws_s3_bucket" "data_bucket" {
  bucket_prefix = "nc-de-data-drop"
}

resource "aws_s3_bucket" "output_bucket" {
  bucket_prefix = "nc-de-data-output"
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "etl/function.zip"
  source = "${path.module}/../function.zip"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.data_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.etl.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.allow_s3]
}
