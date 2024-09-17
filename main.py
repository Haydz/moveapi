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

dynamodb = boto3.client('dynamodb')

table = dynamodb.create_table(
   TableName='Movies',
    AttributeDefinitions=[
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
            {
            'AttributeName': 'title',
            'AttributeType': 'N'
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