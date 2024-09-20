import boto3
import zipfile
# need to create permissions
#need to create file of lambda

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



with zipfile.ZipFile('spam.zip', 'w') as myzip:
    myzip.write('handler.py')

client = boto3.client('lambda')

# response = client.create_function( 
#     FunctionName='PullMovies',
#     Runtime='python3.12'
#     Role='TBD',
#     Handler='lambda',
#     # need to figure out how to create
#     Code={
#         'ZipFile': b'bytes',
#         'S3Bucket': 'string',
#         'S3Key': 'string',
#         'S3ObjectVersion': 'string',
#         'ImageUri': 'string'
#     },
#     Description='string',
#     Timeout=20,
#     MemorySize=123,
#     Publish=True|False,
#     PackageType='Zip',
# )