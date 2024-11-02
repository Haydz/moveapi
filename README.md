# Movie API in AWS SDK (Python) and in Terraform


## Description
This is a project from the [Learn to Cloud Guide](https://learntocloud.guide/) (old version) phase 2 "Programming".

The capstone project is "Create an API with serverless functions that display movie information".

This was completed in both the AWS SDK in Python and via Terraform. 

### High Level Architecture
S3 Bucket:
* An S3 bucket is created, an image uploaded and a Pre signed URL created.
* A Dynamodb is created and Movie information such as title, year and the image pre signed URL is stored
* An AWS Lambda is created with the relevant permissions that will collect that data and print the JSON data.



## Python Version
Below will explain how the python code works as well as decision making.
Find the code within the `/python` directoy.

### main.py
(Named from my habit with Terraform)

```python
import boto3
import create_lambda
import logging
from botocore.exceptions import ClientError
import sys
```
The above code:

* The AWS SDK for Python known as Boto3 is imported so that it can be used
* the create_lambda file is imported so that it can be used to create a lambda (explained later)
* The python logging library is important for logging purposes
* botocore.exceptions is imported from the ClientError library to allow it to be used
* Using the sys module to gracefully exist

```python
logging.basicConfig(level=logging.INFO)
bucket_name= 'haydn-test-stuff' # bucket to upload image file too
filename = 'fear.jpg' #name of image file
image = "https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg" # image URL
tableName = "Movies" # name of table for Dynamodb
bucket_name= 'haydn-test-stuff' # bucket to upload image file too
filename = 'fear.jpg' #name of image file
image = "https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg" # image URL
tableName = "Movies" # name of table for Dynamodb
```
`logging.basicConfig(level=logging.INFO)` configures the logging system with a basic setup and sets the logging level to `INFO`
Variables are used in the above code to be aligned with the DRY principle. That is, instead of changing every single location where the bucket name is, the variable of `bucket_name` can be updated.


```python
#uploading file into S3
s3 = boto3.client('s3')
print(f'Uploading {filename} to s3 bucket: {bucket_name}' )
#create pre sign url
s3 = boto3.client('s3')
try:
    response = s3.upload_file(filename, bucket_name, filename )
except ClientError as e:
        logging.error(e)
# Presigned URL that will last 5 minutes. So that it can be included in the Dynamodb table
print(f'Creating Presigned URL for {filename}' )
try:
    resp = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key':filename}, ExpiresIn=180)
    presigned_url = resp
except ClientError as e:
        logging.error(e)
print(f'The presigned url is {presigned_url}')
```
The above section is for uploading the image file to an S3 bucket and creating a pre-signed URL. The S3 pre signed URL will be used within the Dynamodb table, since images cannot be stored there.



```python
# Creating the Dynamodb table for data to be entered.
dynamodb = boto3.client('dynamodb')

# Before writing to the table, it needs to exist!
# All tables are listed and parsed for the table.
# This is a faster way than using table exists, to identify the table. 
tableList= dynamodb.list_tables()
tableFound = False
for table in tableList["TableNames"]:
    if tableName == table:
        print(f"Table Found: {tableName}, no need to create!")
        tableFound = True
        break
    else:
        continue
#if table is not found, create it
if tableFound == False:
    print("creating table")
    table = dynamodb.create_table(
    TableName=tableName,
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
                {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'
            },
                    {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            },

        ],
        BillingMode='PAY_PER_REQUEST'
    )
    print("waiting for table to exist")
    waiter = dynamodb.get_waiter('table_exists')

    waiter.wait(
        TableName='string',
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts': 30
        }
    )
    tableFound = True
```

This section initializes a client (low level) API for Dynamodb.
It also checks if a table exists (this is quicker than using table exists). If the table does not exist, it is created using the Dynamodb client `create_table` operation.

`PAY_PER_REQUEST` is used because it is only expected to be run for this project.

The code then checks if the table exists once every 30 seconds, for up to 10 times.


```python
# If the table exists, it can have data written:
print("writing data")
# We add data to the Dynamodb table
if tableFound == True:
    response = dynamodb.batch_write_item(
        RequestItems={
            tableName: [
                {
                    'PutRequest': {
                        'Item': {
                            'year': {
                                'N': '1996',
                            },
                            'title': {
                                'S': 'Fear',
                            },
                            'image': {
                                'S': presigned_url,
                            },
                        },
                    },
                },
                            {
                    'PutRequest': {
                        'Item': {
                            'year': {
                                'N': '1979',
                            },
                            'title': {
                                'S': 'Alien',
                            },
                        },
                    },
                },
            ]
        },
    )
```

The above code then attempts to add data to the table if it exists. The `batch_write_item` operation is used to write 2 movies.

```python
# We test that data has been inputted correctly with get_item
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
    print(response_get)
except:
    print("Error getting data")

if "Item" in response_get:
    year = response_get['Item']['year']['N']
    title = response_get['Item']['title']['S']
    image = response_get['Item']['image']['S']

    print(f"The data back is {year} and {title} ")
    print(f'The image url is: {presigned_url}')
    print("Confirmed data has been added.\n ==Now creating the Lambda==")
else:
    print("Data not found")
```

The above code attempts to get the data. This is to ensure that the data has completed successfully. This ensures that we can create the lambda and the data is definetly there. This allows us to not need to trouble shoot the data if the lambda is having any issues.

This was also used as a way to learn getting data within the AWS SDK, outside of the lambda creation.

```python
create_lambda.make_lambda(tableName)
```
If no issues are found, he `make_lambda` function is called from the `create_lambda` package.

** note to self -> have the application terminate if the data is not found**


### create_lambda.py
This is the code that creates the Lambda and correct permissions within AWS.


```python
import boto3
import zipfile
import json
import os
```
Again, the above code imports the required packages/functionality for the script to work.


```python
policyName = 'haydn_access_dynamodb' #name of policy to be created
roleName = 'haydn_lambda_execution_role' #name of execution role to be created
source_file = 'lambda_function.py' # file name of lambda code to be written
functionName = 'haydn_movie_api2' # name of lambda function to be created
```
The variables above allow them to be used in multiple locations. These can be customed if you choose to run this in your own enviornment.



```python
iam = boto3.client('iam')
```
An IAM client is created using the AWS SDK boto3, allowing interaction with AWS Identity and Access Management (IAM) services.


```python
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
        
```
The above code uses the iam client and delete_role_policy and delete_role operation to attempt to delete any role and or policy with the same name. 


```python
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
```

A role needs to be created to allow the lambda to assume it (permissions are created and attached below). This is the trust resource part of the policy.

```python
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
```
The above are the permissions to be used in policy creation and then attached to a role.

Currently these are over permissioned.
** TO  DO ** remove dynamodb permissions,. except for get item.



```python
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

```
The above is using the iam create_role operation to create the role from above. The iam put_role_policy attaches the policy from above to the role. `json.dumps` is used to convert the string into a JSON object.

### Lambda Code:
```python 
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

with open(source_file, 'w') as file1:
    # Writing data to a file
    file1.write(lambda_code)
```
The above string is the code that will be used to create the lambda function. It is included here instead of a seperate file so that the file writing function in Python can be demonstrated.


```python
 os.chmod(source_file, 0o755)

with zipfile.ZipFile('code.zip', 'w',zipfile.ZIP_DEFLATED) as myzip:
    myzip.write(source_file,arcname=os.path.basename(source_file))

with zipfile.ZipFile('code.zip', 'r') as z:
        print(z.namelist())
```
The above code created the zip file that is required to create the lambda function. The files permissions are changed so that it can be accessed by the python.


```python
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
```
The above code checks if a function with the same name exists, and if it does, it deletes it. 
The lamda is created using the Role and policy created earlier as well as with the zipped python function.

The timeout is increased to 20 seconds to allow the Lambda function to connect to the Dynamodb table and pull the data.
