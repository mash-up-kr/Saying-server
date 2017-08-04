import boto3
from Saying.secret import *

s3 = boto3.resource('s3',
                    aws_access_key_id=AWS_S3_ID,
                    aws_secret_access_key=AWS_S3_PWD)
bucket = s3.Bucket(AWS_S3_NM)


def get_s3_object():
    for obj in bucket.objects.all():
        img = obj.key.split('/')[-1]
        if img:
            print(img[:36])
