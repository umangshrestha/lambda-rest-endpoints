variable "aws_access_key" {
  type        = string
  description = "AWS Access Key"
  default     = "test"
  sensitive   = true
}

variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Key"
  default     = "test"
  sensitive   = true
}

variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "us-east-1"
}