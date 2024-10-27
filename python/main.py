
import boto3
import json
import create_lambda
import logging
from botocore.exceptions import ClientError


bucket_name= 'haydn-test-stuff' # bucket to upload image file too
filename = 'fear.jpg' #name of image file
image = "https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg" # image URL
tableName = "Movies" # name of table for Dynamodb

# uploading file into S3
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
      


# Creating the Dynamodb table for data to be entered.
dynamodb = boto3.client('dynamodb')

# === USED FOR DELETING TABLE ===
# because of the way the SDK works, we want to be able to delete the table easily during development.
# try: 
#     response = dynamodb.delete_table(
#         TableName=tableName,
#     )
#     print("Table deleted")
#     waiter = dynamodb.get_waiter('table_not_exists')

#     waiter.wait(
#         TableName=tableName,
#         WaiterConfig={
#             'Delay': 5,
#             'MaxAttempts': 10
#         }
# )
# except:
#     print("table did not exist")

# waiter = dynamodb.get_waiter('table_not_exists')

# waiter.wait(
#     TableName=tableName,
#     WaiterConfig={
#         'Delay': 5,
#         'MaxAttempts': 10
#     }
# )
#===============


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


# a call to create_lambda is made to create the lambda to show
# functionality of a lambda connecting to Dynamodb


create_lambda.make_lambda(tableName)
# ==== deleting always to save money==
# print("Deleting again")
# response = dynamodb.delete_table(
#     TableName=tableName
# )

# waiter = dynamodb.get_waiter('table_not_exists')

# waiter.wait(
#     TableName=tableName,
#     WaiterConfig={
#         'Delay': 5,
#         'MaxAttempts': 10
#     }
# )



# example data
#{"Title":"Dragon","Year":"2011","Rated":"R","Released":"04 Jul 2011","Runtime":"98 min","Genre":"Action, Crime, Drama","Director":"Peter Ho-Sun Chan","Writer":"Oi-Wah Lam, Joyce Chan","Actors":"Donnie Yen, Takeshi Kaneshiro, Tang Wei","Plot":"A papermaker gets involved with a murder case concerning two criminals leading to a determined detective suspecting him and the former's vicious father searching for him.","Language":"Mandarin","Country":"Hong Kong, China","Awards":"14 wins & 21 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BMTc4OTUxMDQ1NF5BMl5BanBnXkFtZTcwOTczMDI2OA@@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.0/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"62/100"}],"Metascore":"62","imdbRating":"7.0","imdbVotes":"15,881","imdbID":"tt1718199","Type":"movie","DVD":"N/A","BoxOffice":"$11,137","Production":"N/A","Website":"N/A","Response":"True"}
# {"Title":"Alien","Year":"1979","Rated":"R","Released":"22 Jun 1979","Runtime":"117 min","Genre":"Horror, Sci-Fi","Director":"Ridley Scott","Writer":"Dan O'Bannon, Ronald Shusett","Actors":"Sigourney Weaver, Tom Skerritt, John Hurt","Plot":"After investigating a mysterious transmission of unknown origin, the crew of a commercial spacecraft encounters a deadly lifeform.","Language":"English","Country":"United Kingdom, United States","Awards":"Won 1 Oscar. 19 wins & 22 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BOGQzZTBjMjQtOTVmMS00NGE5LWEyYmMtOGQ1ZGZjNmRkYjFhXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.5/10"},{"Source":"Rotten Tomatoes","Value":"93%"},{"Source":"Metacritic","Value":"89/100"}],"Metascore":"89","imdbRating":"8.5","imdbVotes":"978,948","imdbID":"tt0078748","Type":"movie","DVD":"N/A","BoxOffice":"$84,206,106","Production":"N/A","Website":"N/A","Response":"True"}
# {"Title":"Fear","Year":"1996","Rated":"R","Released":"12 Apr 1996","Runtime":"97 min","Genre":"Drama, Thriller","Director":"James Foley","Writer":"Christopher Crowe","Actors":"Mark Wahlberg, Reese Witherspoon, William Petersen","Plot":"When Nicole met handsome, charming, affectionate David, he was everything. It seemed perfect, but soon she sees that David has a darker side. And his adoration turns to obsession, their dream into a nightmare, and her love into fear.","Language":"English","Country":"United States, Canada","Awards":"1 win & 2 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"6.2/10"},{"Source":"Rotten Tomatoes","Value":"46%"},{"Source":"Metacritic","Value":"51/100"}],"Metascore":"51","imdbRating":"6.2","imdbVotes":"56,259","imdbID":"tt0116287","Type":"movie","DVD":"N/A","BoxOffice":"$20,831,000","Production":"N/A","Website":"N/A","Response":"True"}

