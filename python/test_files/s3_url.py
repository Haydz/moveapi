import boto3
import logging
from botocore.exceptions import ClientError


dynamodb = boto3.client('s3')
image = "https://m.media-amazon.com/images/M/MV5BZTM4ZmJmMTQtMWUxOS00MjQxLTllNmQtNzI4YWVhYzZlNTRkXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_SX300.jpg"
bucket_name= 'haydn-test-stuff'
filename = 'fear.jpg'

#wget image locally
#need to upload into bucket

#create pre sign url

s3 = boto3.client('s3')
try:
    response = s3.upload_file(filename, bucket_name, filename )
except ClientError as e:
        logging.error(e)



resp = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key':filename}, ExpiresIn=180)
print(resp)
# try:
#     response = s3.get_object(Bucket=bucket_name, Key=filename)
# except ClientError as e:
#         logging.error(e)






#===For deleting ===
# try: 
#     response = s3.delete_object(
#         Bucket=bucket_name,
#         Key=filename,
        
#     )
# except ClientError as e:
#         logging.error(e)

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html