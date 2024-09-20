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
