variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "handler" {
  description = "The function entrypoint in your code"
  type        = string
}

variable "iam_role_arn" {
  description = "The ARN of the IAM role that the Lambda function assumes"
  type        = string
}

variable "runtime" {
  description = "The runtime environment for the Lambda function"
  type        = string
}

# variable "environment_variables" {
#   description = "Environment variables for the Lambda function"
#   type        = map(string)
#   default     = {}
# }
