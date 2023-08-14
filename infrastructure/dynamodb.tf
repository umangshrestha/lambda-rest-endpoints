resource "aws_dynamodb_table" "todos" {
  name           = "TODO"
  hash_key       = "id"
  read_capacity  = 1
  write_capacity = 1

  server_side_encryption {
    enabled = true
  }

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "TODO"
    Environment = "dev"
  }
}
