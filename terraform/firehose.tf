# resource "aws_kinesis_firehose_delivery_stream" "firehose_stream" {
#   name        = "classification-stream"
#   destination = "extended_s3"

# extended_s3_configuration {
#     role_arn   = aws_iam_role.firehose_role.arn
#     bucket_arn = aws_s3_bucket.classification_bucket.arn

#     processing_configuration {
#       enabled = "true"

#       processors {
#         type = "Lambda"

#         parameters {
#           parameter_name  = "LambdaArn"
#           parameter_value = "${aws_lambda_function.lambda_processor.arn}:$LATEST"
#         }
#       }
#     }
#   }
# }