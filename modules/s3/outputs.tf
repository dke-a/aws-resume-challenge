output "bucket_arn" {
  value       = length(aws_s3_bucket.bucket) > 0 ? aws_s3_bucket.bucket[0].arn : ""
  description = "The ARN of the S3 bucket"
}

output "bucket_id" {
  value       = length(aws_s3_bucket.bucket) > 0 ? aws_s3_bucket.bucket[0].id : ""
  description = "The ID of the S3 bucket"
}
