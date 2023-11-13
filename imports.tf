# import {
#   to = module.resume_bucket.aws_s3_bucket.this[0]
#   id = "cloudresume-don"
# }

# import {
#   to = module.resume_bucket.aws_s3_bucket_versioning.this[0]
#   id = "cloudresume-don"
# }

# import {
#   to = module.cloudfront_resume.aws_cloudfront_distribution.this[0]
#   id = "ER0K5G3S0PD5R"
# }

# import {
#   to = module.ddb_resume_table.aws_dynamodb_table.this[0]
#   id = "visitCounter"
# }

# import {
#   to = module.apigw_resume.aws_apigatewayv2_api.this[0]
#   id = "9drbe81ae7"
# }

# import {
#   to = module.lambda_resume_update_counts.aws_lambda_function.this[0]
#   id = "countVisit"
# }

# module "lambda_resume_update_count" {
#   create = true
#   source        = "terraform-aws-modules/lambda/aws"
#   function_name = "countVisit"
#   handler       = "lambda_function.lambda_handler"
# }


# import {
#     to = aws_cloudfront_distribution.cf_distribution
#     id = "ER0K5G3S0PD5R"
# }



# import {
#     to = module.resume_bucket.aws_s3_bucket.bucket[0]
#     id = "cloudresume-don"
# }

# import{
#     to = module.resume_bucket.aws_s3_bucket_acl.bucket_acl
#     id = "cloudresume-don"
# }

# module "resume_bucket" {
#   source = "./modules/s3"

#   bucket_name       = "cloudresume-don"
#   #bucket_policy     = data.aws_iam_policy_document.s3_policy.json
#   bucket_acl        = "private"
#   sse_algorithm     = "AES256"
#   versioning_status = "Disabled"
# }


# output "s3_bucket_arn" {
#   value = module.s3_bucket.s3_bucket_arn
#   description = "The ARN of the S3 bucket"
# }

# import {
#     to = aws_dynamodb_table.visit_counter
#     id = "visitCounter"
# }

# import {
#     to = aws_cloudfront_distribution.cf_distribution
#     id = "ER0K5G3S0PD5R"
# }

# import {
#     to = aws_apigatewayv2_api.apigw
#     id = "9drbe81ae7"
# }

# import {
#     to = aws_lambda_function.lambda_update_count
#     id = "countVisit"
# }
