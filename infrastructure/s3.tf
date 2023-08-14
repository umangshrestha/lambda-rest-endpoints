resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "lambda-bucket"
}

resource "aws_s3_object" "lambda_bucket_object" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "lambda.zip"
  source = data.archive_file.lambda_zip.output_path
}
