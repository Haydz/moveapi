terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# create inline policy for role and role
resource "aws_iam_role" "test_role" {
  name = "haydn_lambda_execution_role_tf"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })

}




data "aws_iam_policy_document" "inline_policy" {
  statement {
    actions   = ["ec2:DescribeAccountAttributes"]
    resources = ["*"]
  }
}


#aws_iam_role_policy

resource "aws_iam_role_policy" "test_policy" {
  name = "haydn_access_dynamodb_tf"
  role = aws_iam_role.test_role.id

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "ReadWriteTable",
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        "Resource" : "arn:aws:dynamodb:*:*:table/Movies"
      },
      {
        "Sid" : "GetStreamRecords",
        "Effect" : "Allow",
        "Action" : "dynamodb:GetRecords",
        "Resource" : "arn:aws:dynamodb:*:*:table/Movies/stream/* "
      },
      {
        "Sid" : "WriteLogStreamsAndGroups",
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "CreateLogGroup",
        "Effect" : "Allow",
        "Action" : "logs:CreateLogGroup",
        "Resource" : "*"
      }
    ]
  })
}

# need to create dynamodb

resource "aws_dynamodb_table" "db_example" {
  name           = "Movies_tf"
  
 
  billing_mode   = "PAY_PER_REQUEST"
  stream_enabled = false

hash_key       = "year"
  attribute {
    name = "year"
    type = "N"
  }

range_key      = "title"
  attribute {
    name = "title"
    type = "S"
  }
  
}
# need to add to table



resource "aws_dynamodb_table_item" "example_year" {
  table_name = aws_dynamodb_table.db_example.name
  hash_key   = "year"
  range_key  = "title"  # Also include the range_key

  item = jsonencode({
    "year": {"N": "1990"},
    "title": {"S": "fear"},
    "year": {"N": "1985"},
    "title": {"S": "BBQ"},

  
 })
}


# resource "aws_dynamodb_table_item" "example_title" {
#   table_name = aws_dynamodb_table.db_example.name
#   hash_key   = aws_dynamodb_table.db_example.hash_key

#   item = <<ITEM
#   {
#   "title": {"S": "Fear"}
#  }
# ITEM
# }


# need to create lambda
#associate the role with labda
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "handler.py"
  output_path = "code.zip"
}



resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = data.archive_file.lambda.output_path
  function_name = "haydn_movie_api2_tf"
  role          = aws_iam_role.test_role.arn
  handler       = "handler.lambda_handler"
  source_code_hash = filebase64sha256(data.archive_file.lambda.output_path)
  runtime = "python3.12"


}