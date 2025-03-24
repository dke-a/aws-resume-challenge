locals {
  mime_types = {
    "html" = "text/html",
    "css"  = "text/css",
    "js"   = "application/javascript",
    "png"  = "image/png",
    "jpg"  = "image/jpeg",
    "svg"  = "image/svg+xml",
    // Add other file extensions and MIME types as needed
  }
}

# S3 Bucket Module Configuration
module "resume_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"
  bucket = "cloudresume-don"

  # Versioning to be enabled once VC is setup.
  versioning = {
    enabled    = true
    mfa_delete = false
  }
}


# resource "aws_s3_object" "s3_resume_object" {
#   for_each = fileset("${path.module}/s3_resume_bucket_files", "*")

#   bucket = "cloudresume-don"                                     # Specify your S3 bucket name
#   key    = each.value                                            # The key (path) in the bucket
#   source = "${path.module}/s3_resume_bucket_files/${each.value}" # Path to the local file
#   etag   = filemd5("${path.module}/s3_resume_bucket_files/${each.value}")
# }

resource "aws_s3_object" "s3_resume_object" {
  for_each = fileset("${path.module}/s3_resume_bucket_files", "**/*")

  bucket       = "cloudresume-don"
  key          = each.value
  source       = "${path.module}/s3_resume_bucket_files/${each.value}"
  etag         = filemd5("${path.module}/s3_resume_bucket_files/${each.value}")
  content_type = lookup(local.mime_types, split(".", each.value)[1], "binary/octet-stream")
}

# CloudFront Distribution Module Configuration
module "cloudfront_resume" {
  source              = "terraform-aws-modules/cloudfront/aws"
  aliases             = ["*.donangeles.com", "donangeles.com"]
  comment             = null
  default_root_object = "index.html"
  enabled             = true
  http_version        = "http2and3"
  is_ipv6_enabled     = true
  price_class         = "PriceClass_All"
  retain_on_delete    = false
  wait_for_deployment = true
  web_acl_id          = null

  # Origin configuration pointing to the S3 bucket
  origin = {
    content = {
      domain_name              = "cloudresume-don.s3.us-east-1.amazonaws.com"
      origin_access_control_id = "E2RU6J1N6S39CV"
      origin_id                = "cloudresume-don.s3-website-us-east-1.amazonaws.com"
    }
  }

  # Default cache behavior settings
  default_cache_behavior = {
    allowed_methods        = ["GET", "HEAD"]
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "cloudresume-don.s3-website-us-east-1.amazonaws.com"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    use_forwarded_values   = false
  }

  # Viewer certificate configuration
  viewer_certificate = {
    acm_certificate_arn            = "arn:aws:acm:us-east-1:408810908626:certificate/90e8be72-67ba-4297-9d7f-31d095a46fbd"
    cloudfront_default_certificate = false
    iam_certificate_id             = null
    minimum_protocol_version       = "TLSv1.2_2021"
    ssl_support_method             = "sni-only"
  }
}

# DynamoDB Table Module Configuration
module "ddb_resume_table" {
  source = "terraform-aws-modules/dynamodb-table/aws"
  name   = "visitCounter"

  # Setting timeouts and tags explicitly to override module defaults
  timeouts = {}
  tags     = null
}

# API Gateway Module Configuration
module "apigw_resume" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "2.1.0"  # ✅ Use the latest stable version

  name   = "visitorCounterAPI"

  cors_configuration = {
    allow_headers = ["'content-type,x-amz-date,authorization,x-api-key,x-amz-security-token'"]
    allow_methods = ["POST", "OPTIONS", "GET"]
    allow_origins = ["https://www.donangeles.com", "https://donangeles.com"]
  }

  create_api_domain_name         = false
  create_default_stage           = false
  create_routes_and_integrations = true

  integrations = {
    "POST /countVisit" = {
      lambda_arn             = aws_lambda_function.lambda_update_count.arn
      connection_type        = "INTERNET"
      integration_type       = "AWS_PROXY"
      payload_format_version = "2.0"
      timeout_milliseconds   = 30000
    }

    "OPTIONS /countVisit" = {
      lambda_arn             = aws_lambda_function.lambda_update_count.arn
      connection_type        = "INTERNET"
      integration_type       = "AWS_PROXY"
      payload_format_version = "2.0"
      timeout_milliseconds   = 30000
    }
  }
}

# AWS Lambda Function Resource Configuration
resource "aws_lambda_function" "lambda_update_count" {
  function_name = "countVisit"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  role          = "arn:aws:iam::408810908626:role/lambda-ddb-visitcount"
  memory_size   = 128
  timeout       = 3
  package_type  = "Zip"
  #source_code_hash                   = "GpCmZ2hqv/4gy/RvyxrfWF2vq4r1wM6oo+k52y4OcrA="
  filename         = data.archive_file.update_count_zip.output_path         #"${path.module}/lambda_functions/update_count.zip" 
  source_code_hash = data.archive_file.update_count_zip.output_base64sha256 #filebase64sha256("${path.module}/lambda_functions/update_count.zip")

  # Additional configuration details
  architectures                  = ["x86_64"]
  reserved_concurrent_executions = -1
  ephemeral_storage {
    size = 512
  }
  tracing_config {
    mode = "PassThrough"
  }

}

data "archive_file" "update_count_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/update_count"
  output_path = "${path.module}/lambda_functions/builds/update_count.zip"
}

output "lambda_function_source_code_hash" {
  description = "The base64-encoded SHA256 hash of the Lambda function's source code"
  value       = aws_lambda_function.lambda_update_count.source_code_hash
  #data.archive_file.update_count_zip.output_base64sha256 
  #filebase64sha256("${path.module}/lambda_functions/update_count.zip") 
  #aws_lambda_function.lambda_update_count.source_code_hash
}
