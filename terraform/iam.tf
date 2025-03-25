
# data "aws_iam_policy_document" "firehose_assume_role" {
#   statement {
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["firehose.amazonaws.com"]
#     }

#     actions = ["sts:AssumeRole"]
#   }
# }

# resource "aws_iam_role" "firehose_role" {
#   name               = "firehose_test_role"
#   assume_role_policy = data.aws_iam_policy_document.firehose_assume_role.json
# }

# resource "aws_iam_policy" "firehose_s3_policy" {
#   name = "firehose_s3_policy"

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Action = [
#           "s3:PutObject",
#           "s3:GetBucketLocation",
#           "s3:ListBucket"
#         ]
#         Resource = [
#           aws_s3_bucket.classification_bucket.arn,
#           "${aws_s3_bucket.classification_bucket.arn}/*"
#         ]
#       }
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "firehose_s3_attach" {
#   role       = aws_iam_role.firehose_role.name
#   policy_arn = aws_iam_policy.firehose_s3_policy.arn
# }


# data "aws_iam_policy_document" "lambda_assume_role" {
#   statement {
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }

#     actions = ["sts:AssumeRole"]
#   }
# }

# resource "aws_iam_role" "lambda_iam" {
#   name               = "lambda_iam"
#   assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
# }