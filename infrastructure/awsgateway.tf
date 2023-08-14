resource "aws_apigatewayv2_api" "lambda_api" {
  name    = "lambda-api"
  protocol_type = "HTTP"
  description = "API for Lambda"
}

resource "aws_apigatewayv2_integration" "hello_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.hello.invoke_arn
}

resource "aws_apigatewayv2_integration" "create_todo_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.create_todo.invoke_arn
}

resource "aws_apigatewayv2_integration" "get_todo_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.get_todo.invoke_arn
}

resource "aws_apigatewayv2_integration" "get_todos_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.get_todos.invoke_arn
}

resource "aws_apigatewayv2_integration" "update_todo_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.update_todo.invoke_arn
}

resource "aws_apigatewayv2_integration" "delete_todo_integration" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.delete_todo.invoke_arn
}

resource "aws_apigatewayv2_route" "hello_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "GET /hello/{name}"
  target = "integrations/${aws_apigatewayv2_integration.hello_integration.id}"
}

resource "aws_apigatewayv2_route" "create_todo_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "POST /todo"
  target = "integrations/${aws_apigatewayv2_integration.create_todo_integration.id}"
}

resource "aws_apigatewayv2_route" "get_todos_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "GET /todo"
  target = "integrations/${aws_apigatewayv2_integration.get_todos_integration.id}"
}

resource "aws_apigatewayv2_route" "get_todo_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "GET /todo/{id+}"
  target = "integrations/${aws_apigatewayv2_integration.get_todo_integration.id}"
}

resource "aws_apigatewayv2_route" "update_todo_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "PUT /todo/{id+}"
  target = "integrations/${aws_apigatewayv2_integration.update_todo_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_todo_route" {
  api_id = aws_apigatewayv2_api.lambda_api.id
  route_key = "DELETE /todo/{id+}"
  target = "integrations/${aws_apigatewayv2_integration.delete_todo_integration.id}"
}

resource "aws_lambda_permission" "apigateway_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = aws_apigatewayv2_api.lambda_api.execution_arn
}

resource "aws_apigatewayv2_stage" "lambda_api_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "dev"
  auto_deploy = true
}
