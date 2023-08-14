provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.aws_region

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  skip_region_validation      = true

  endpoints {
    apigateway     = local.localstack_host
    apigatewayv2   = local.localstack_host
    cloudformation = local.localstack_host
    cloudwatch     = local.localstack_host
    dynamodb       = local.localstack_host
    ec2            = local.localstack_host
    es             = local.localstack_host
    firehose       = local.localstack_host
    iam            = local.localstack_host
    kinesis        = local.localstack_host
    lambda         = local.localstack_host
    rds            = local.localstack_host
    redshift       = local.localstack_host
    route53        = local.localstack_host
    s3             = local.s3_bucket_host
    secretsmanager = local.localstack_host
    ses            = local.localstack_host
    sns            = local.localstack_host
    sqs            = local.localstack_host
    ssm            = local.localstack_host
    stepfunctions  = local.localstack_host
    sts            = local.localstack_host
  }
}


