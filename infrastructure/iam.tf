resource "aws_iam_role" "lambda_exec" {
  name = "run-lambda-handler"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}


resource "aws_iam_role" "dynamodb_readonly" {
  name = "dynamodb-read-only"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
        ]
        resource = aws_dynamodb_table.todos.arn
        Effect   = "Allow"
        Sid      = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}


resource "aws_iam_role" "dynamodb_readwrite" {
  name = "dynamodb-read-write"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        resource = aws_dynamodb_table.todos.arn
        Effect   = "Allow"
        Sid      = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}