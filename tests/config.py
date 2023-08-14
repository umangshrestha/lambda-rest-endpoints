import boto3
ENDPOINT_URL='http://localhost:4566'


lambda_client = boto3.client('lambda', 
    region_name='us-east-1', 
    endpoint_url=ENDPOINT_URL)

apigatewayv2_client = boto3.client('apigatewayv2',
    region_name='us-east-1',
    endpoint_url=ENDPOINT_URL)

api_id = apigatewayv2_client.get_apis()['Items'][0]['ApiId']

base_url = f"https://localhost:4566/restapis/{api_id}/prod/_user_request_"
