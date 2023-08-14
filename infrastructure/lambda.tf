locals {
  files = [
    "../src/hello.py",
    "../src/create_todo.py",
    "../src/get_todo.py",
    "../src/get_todos.py",
    "../src/delete_todo.py",
    "../src/update_todo.py",
    "../src/utils/timestamp.py",
    "../src/utils/__init__.py",
  ]
  md5_sums = [for f in local.files : md5(file(f))]
  dir_name = md5(join("", local.md5_sums))
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "./artifacts/${local.dir_name}.zip"
}


resource "aws_lambda_function" "hello" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "hello"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "hello.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}


resource "aws_lambda_function" "create_todo" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "create_todo"
  role             = aws_iam_role.dynamodb_readwrite.arn
  handler          = "create_todo.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}

resource "aws_lambda_function" "get_todo" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "get_todo"
  role             = aws_iam_role.dynamodb_readonly.arn
  handler          = "get_todo.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}

resource "aws_lambda_function" "get_todos" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "get_todos"
  role             = aws_iam_role.dynamodb_readonly.arn
  handler          = "get_todos.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}


resource "aws_lambda_function" "delete_todo" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "delete_todo"
  role             = aws_iam_role.dynamodb_readwrite.arn
  handler          = "delete_todo.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}

resource "aws_lambda_function" "update_todo" {
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_object.id

  function_name    = "update_todo"
  role             = aws_iam_role.dynamodb_readwrite.arn
  handler          = "update_todo.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
}
  