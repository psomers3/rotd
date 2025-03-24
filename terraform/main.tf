terraform {
  required_version = ">= 1.3"
  backend "s3" {
    region = "us-east-1"
    bucket = "my-bucket"
    key = "terraform_state.tfstate"
  }
}
