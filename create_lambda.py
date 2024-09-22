import boto3
import zipfile
import json
import os

#lamba code file


def make_lambda():



    source_file = 'lambda_function.py'

    #Getting account Number:
    sts = boto3.client("sts")
    response = sts.get_caller_identity()
    account_number = response["Account"]


    iam = boto3.client('iam')
    role_name = 'haydn_lambda_execution_role'



    print("attempting to delete the inline poliy and role.")

    try:
        response = iam.delete_role_policy(
            RoleName=role_name,
            PolicyName='haydn_access_dynamodb'
        )
        print("Policy existed, role delted.")
    except:
        print("couldnt delete inline policy")

    try:
        response = iam.delete_role(
            RoleName=role_name
        )
        print("Role existed, deleted.")
    except:
        print('couldnt delete role')
    #need to create file of lambda
    # need to create permissions

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

    logs_policy={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "logs:CreateLogGroup",
                "Resource": "arn:aws:logs:us-east-1:{account_number}:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:us-east-1:{account_number}:log-group:/aws/lambda/haydn_movie_api:*"
                ]
            }
        ]
    }


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
                "Resource": "arn:aws:dynamodb:*:*:table/Movies"
            },
            {
                "Sid": "GetStreamRecords",
                "Effect": "Allow",
                "Action": "dynamodb:GetRecords",
                "Resource": "arn:aws:dynamodb:*:*:table/Movies/stream/* "
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





    # Program to show various ways to
    # write data to a file using with statement

    lambda_code = """
    import json
    import boto3

    def lambda_handler(event, context):
        tableName = "Movies"
        dynamodb = boto3.client('dynamodb')
        response_get = None
        print("attempting to get data")
        try:
            response_get = dynamodb.get_item(
                Key={
                    'year': {
                        'N': '1996',
                    },
                    'title': {
                        'S': 'Fear',
                    },
                },
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
        
                print(f"The data back is {year} and {title} ")
            else:
                print("Data not found")

        return {
            'statusCode': 200,
            'body': json.dumps(f"The data back is {year} and {title} " )
        }
    """

    # Writing to file
    with open("handler.py", 'w') as file1:
        # Writing data to a file
        file1.write(lambda_code)

    try:
        execution_creation = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(execution_role)
        )
        exec_role_arn = execution_creation['Role']['Arn']
        print(exec_role_arn)
    except:
        exit()

    try:
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName="haydn_access_dynamodb",
            PolicyDocument=json.dumps(iam_policy)
        )
    except:
        print("policy not attached")


    with zipfile.ZipFile('code.zip', 'w',zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(source_file,arcname=os.path.basename(source_file))

    with zipfile.ZipFile('code.zip', 'r') as z:
        print(z.namelist())

    os.chmod(source_file, 0o755)
    # os.chmod("code.zip", 0o755)

    client = boto3.client('lambda')



    print("deleting function for fresh start")

    try:
        client.delete_function(
        FunctionName='haydn_movie_api2'
        )
    except:
        print("Could not delete function")

    with open('code.zip', 'rb') as f:
        zipped_code = f.read()

    try:
        response = client.create_function( 
        FunctionName='haydn_movie_api2',
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