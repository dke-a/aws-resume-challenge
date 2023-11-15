resource "aws_s3_bucket" "terraform_state" {
  bucket = "resume-tf-state-bucket"
}

resource "aws_s3_bucket_versioning" "state_bucket_versioning" {
  bucket = module.resume_bucket.s3_bucket_id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name           = "resume_tf_state_lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}