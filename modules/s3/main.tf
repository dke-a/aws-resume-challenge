resource "aws_s3_bucket" "bucket" {
  count  = var.bucket_name != null ? 1 : 0
  bucket = var.bucket_name
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  count  = var.bucket_acl != null ? 1 : 0
  bucket = aws_s3_bucket.bucket[0].id
  acl    = var.bucket_acl
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  count  = var.bucket_policy != null ? 1 : 0
  bucket = aws_s3_bucket.bucket[0].id
  policy = var.bucket_policy
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_sse" {
  count  = var.sse_algorithm != null ? 1 : 0
  bucket = aws_s3_bucket.bucket[0].id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = var.sse_algorithm
    }
  }
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
  count  = var.versioning_status != null ? 1 : 0
  bucket = aws_s3_bucket.bucket[0].id
  versioning_configuration {
    status = var.versioning_status
  }
}


