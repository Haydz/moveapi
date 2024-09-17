#{"Title":"Dragon","Year":"2011","Rated":"R","Released":"04 Jul 2011","Runtime":"98 min","Genre":"Action, Crime, Drama","Director":"Peter Ho-Sun Chan","Writer":"Oi-Wah Lam, Joyce Chan","Actors":"Donnie Yen, Takeshi Kaneshiro, Tang Wei","Plot":"A papermaker gets involved with a murder case concerning two criminals leading to a determined detective suspecting him and the former's vicious father searching for him.","Language":"Mandarin","Country":"Hong Kong, China","Awards":"14 wins & 21 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BMTc4OTUxMDQ1NF5BMl5BanBnXkFtZTcwOTczMDI2OA@@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.0/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"62/100"}],"Metascore":"62","imdbRating":"7.0","imdbVotes":"15,881","imdbID":"tt1718199","Type":"movie","DVD":"N/A","BoxOffice":"$11,137","Production":"N/A","Website":"N/A","Response":"True"}

# {"Title":"Alien","Year":"1979","Rated":"R","Released":"22 Jun 1979","Runtime":"117 min","Genre":"Horror, Sci-Fi","Director":"Ridley Scott","Writer":"Dan O'Bannon, Ronald Shusett","Actors":"Sigourney Weaver, Tom Skerritt, John Hurt","Plot":"After investigating a mysterious transmission of unknown origin, the crew of a commercial spacecraft encounters a deadly lifeform.","Language":"English","Country":"United Kingdom, United States","Awards":"Won 1 Oscar. 19 wins & 22 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BOGQzZTBjMjQtOTVmMS00NGE5LWEyYmMtOGQ1ZGZjNmRkYjFhXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.5/10"},{"Source":"Rotten Tomatoes","Value":"93%"},{"Source":"Metacritic","Value":"89/100"}],"Metascore":"89","imdbRating":"8.5","imdbVotes":"978,948","imdbID":"tt0078748","Type":"movie","DVD":"N/A","BoxOffice":"$84,206,106","Production":"N/A","Website":"N/A","Response":"True"}


# {"Title":"Fear","Year":"1996","Rated":"R","Released":"12 Apr 1996","Runtime":"97 min","Genre":"Drama, Thriller","Director":"James Foley","Writer":"Christopher Crowe","Actors":"Mark Wahlberg, Reese Witherspoon, William Petersen","Plot":"When Nicole met handsome, charming, affectionate David, he was everything. It seemed perfect, but soon she sees that David has a darker side. And his adoration turns to obsession, their dream into a nightmare, and her love into fear.","Language":"English","Country":"United States, Canada","Awards":"1 win & 2 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"6.2/10"},{"Source":"Rotten Tomatoes","Value":"46%"},{"Source":"Metacritic","Value":"51/100"}],"Metascore":"51","imdbRating":"6.2","imdbVotes":"56,259","imdbID":"tt0116287","Type":"movie","DVD":"N/A","BoxOffice":"$20,831,000","Production":"N/A","Website":"N/A","Response":"True"}

#cloud infra
# need dynamodb, s3 website?
#maybe AWS amplify? https://docs.djangoproject.com/en/5.1/intro/tutorial01/

# can cheat and host in ECS?
# lets containerize it

# import requests
# api_key = "7d7abb64"

# respone = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&t=Dragon")

# print(respone.json()).


# need to upload data to S3
# create presigned s3 

# lets start easy, lets create a dynamodb table and add teh data?

#create dynamodb table with year and title.
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_table.html#
import boto3
import json

tableName = "Movies"
dynamodb = boto3.client('dynamodb')

# === USED FOR DELETING TABLE ===
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


# Ensuring Table exists
tableList= dynamodb.list_tables()

tableFound = False
for table in tableList["TableNames"]:
    if tableName == table:
        print(f"Table Found: {tableName}, no need to create!")
        tableFound = True
        break
    else:
        continue
#if table is not found, we create it
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


print("writing data")

# We add data to dynamodb
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

    print(f"The data back is {year} and {title} ")
else:
    print("Data not found")







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

