resource "aws_s3_bucket" "raw_images_bucket" {
    bucket = "raw-data"
}

# resource "aws_s3_bucket" "classification_bucket" {
#     bucket = "classification"
# }
# resource "aws_s3_bucket_acl" "classification_bucket_acl" {
#   bucket = aws_s3_bucket.classification_bucket.id
#   acl    = "private"
# }