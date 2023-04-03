import json

import boto3

# バケット名,オブジェクト名
BUCKET_NAME = "test-backet"

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    response = s3_client.get_object(Bucket=BUCKET_NAME)
    body = response["Body"].read()

    return json.loads(body.decode("utf-8"))


def list_backet_images():
    keys = []
    for obj in s3_client.list_objects(Bucket=BUCKET_NAME)["Contents"]:
        keys.append(obj["Key"])
        print(
            obj["Key"],
            obj["Size"],
            obj["LastModified"].strftime("%Y/%m/%d %H:%M:%S"),
        )
    return keys
