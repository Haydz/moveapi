import boto3
import zipfile
import json
import os
import sys

policyName = 'haydn_access_dynamodb' #name of policy to be created
roleName = 'haydn_lambda_execution_role' #name of execution role to be created
source_file = 'lambda_function.py' # file name of lambda code to be written
functionName = 'haydn_movie_api2' # name of lambda function to be created

def make_lambda(tableName):
    #Getting account Number:
    # sts = boto3.client("sts")
    # response = sts.get_caller_identity()
    # account_number = response["Account"]
    # print(f"Creating Lambda ")


    iam = boto3.client('iam')
    # to ensure there are no roles previously named that exist
    print("attempting to delete the inline poliy and role.")
    try:
        response = iam.delete_role_policy(
            RoleName=roleName,
            PolicyName=policyName
        )
        print("Policy existed, role deleted.")
    except:
        print("Couldnt Delete Inline policy")

    try:
        response = iam.delete_role(
            RoleName=roleName
        )
        print("Role existed, deleted.")
    except:
        print('couldnt delete role')
        sys.exit(1)

     
    #execution role permissions. allowed lamnda to assume this role
    execution_role={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    # Iam policy to attach to execution role
    iam_policy= {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "ReadWriteTable",
                "Effect": "Allow",
                "Action": [
                    "dynamodb:BatchGetItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem"
                ],
                "Resource": f"arn:aws:dynamodb:*:*:table/{tableName}"
            },
            {
                "Sid": "GetStreamRecords",
                "Effect": "Allow",
                "Action": "dynamodb:GetRecords",
                "Resource": f"arn:aws:dynamodb:*:*:table/{tableName}/stream/* "
            },
            {
                "Sid": "WriteLogStreamsAndGroups",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "*"
            },
            {
                "Sid": "CreateLogGroup",
                "Effect": "Allow",
                "Action": "logs:CreateLogGroup",
                "Resource": "*"
            }
        ]
    }


    try:
        execution_creation = iam.create_role(
            RoleName=roleName,
            AssumeRolePolicyDocument=json.dumps(execution_role)
        )
        exec_role_arn = execution_creation['Role']['Arn']
        print(exec_role_arn)
    except Exception as e:
        print("Error creating role:", e)
        sys.exit(1)

    try:
        iam.put_role_policy(
            RoleName=roleName,
            PolicyName=policyName,
            PolicyDocument=json.dumps(iam_policy)
        )
    except:
        print("Policy was unable to be attached")
        sys.exit(1)



    # Program to show various ways to
    # write data to a file using with statement
    # code to be created that will get the data from lambda
    # (double curly braces for escaping within f string)
    lambda_code = f"""
import json
import boto3

def lambda_handler(event, context):
    year = ''
    title = ''
    tableName = "{tableName}"
    dynamodb = boto3.client('dynamodb')
    response_get = None
    print("attempting to get data")
    try:
        response_get = dynamodb.get_item(
            Key={{  
                'year': {{
                    'N': '1996',
                }},
                'title': {{
                    'S': 'Fear',
                }},
            }},
            TableName=tableName,
        )
    except:
        print("Error getting data")
    if response_get == None:
        print("nothing found")
    else:
        if "Item" in response_get:
            year = response_get['Item']['year']['N']
            title = response_get['Item']['title']['S']
    
            print(f"The data back is {{year}} and {{title}} ")
        else:
            print("Data not found")

    return {{
        'statusCode': 200,
        'body': json.dumps(f"The data back is {{year}} and {{title}}")
    }}
"""
    
  

    #code needs to be written to a file so that it can be zipped and added to the lambda
    with open(source_file, 'w') as file1:
        # Writing data to a file
        file1.write(lambda_code)
    
    os.chmod(source_file, 0o755)

    with zipfile.ZipFile('code.zip', 'w',zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(source_file,arcname=os.path.basename(source_file))

    with zipfile.ZipFile('code.zip', 'r') as z:
        print(z.namelist())


    # os.chmod("code.zip", 0o755)

    client = boto3.client('lambda')


    # Ensuring there are no Functions with the same name
    print("deleting function for fresh start")
    try:
        client.delete_function(
        FunctionName=functionName
        )
    except:
        print("Could not delete function")

    with open('code.zip', 'rb') as f:
        zipped_code = f.read()

    try:
        response = client.create_function( 
        FunctionName=functionName,
        Runtime='python3.12',
        Role=exec_role_arn,
        Handler='lambda_function.lambda_handler',
        # need to figure out how to create
        Code={
            'ZipFile': zipped_code
        },
        Description='string',
        Timeout=20,
        Publish=True,
        PackageType='Zip'
    )
        print("FUNCTION CREATED")
    except:
        print("function creation failed")