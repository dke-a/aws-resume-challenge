variable "bucket_name" {
  type        = string
  description = "The name of the S3 bucket"
  #default     = null
}

variable "bucket_acl" {
  type        = string
  description = "The ACL of the S3 bucket"
  default     = null
}

variable "bucket_policy" {
  type        = string
  description = "The policy of the S3 bucket, in JSON format"
  default     = null
}

variable "sse_algorithm" {
  type        = string
  description = "The server-side encryption algorithm"
  default     = null
}

variable "versioning_status" {
  type        = string
  description = "The versioning status of the S3 bucket"
  default     = null
}
