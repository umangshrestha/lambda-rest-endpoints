output "api_gateway_invoke_url" {
  value = aws_apigatewayv2_stage.lambda_api_stage.invoke_url
}

output "localstack_hello_world_url" {
  value = tomap({
    "/hello" = "${local.localstack_host}/restapis/${aws_apigatewayv2_api.lambda_api.id}/${aws_apigatewayv2_stage.lambda_api_stage.id}/_user_request_/hello",
    "/todo"  = "${local.localstack_host}/restapis/${aws_apigatewayv2_api.lambda_api.id}/${aws_apigatewayv2_stage.lambda_api_stage.id}/_user_request_/todo",
  })
}


