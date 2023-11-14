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
#   to = aws_apigatewayv2_integration.countVisit
#   id = "9drbe81ae7/2mk7eh1"
# }

# import {
#   to = aws_apigatewayv2_integration.getVisitCount
#   id = "9drbe81ae7/uaxehuj"
# }