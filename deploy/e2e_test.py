import os
import time

import boto3
from boto3.s3.transfer import S3Transfer

BUCKET_NAME = "s3-bucket-for-image-upload"

client = boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
region_name = os.getenv("AWS_DEFAULT_REGION")

transfer = S3Transfer(client)
transfer.upload_file("./lambda/sample/0.jpg", BUCKET_NAME, "0.jpg")

webp_list = []

# Start a loop to check if the file conversion is complete,
# retrying every 3 seconds if not.
for i in range(5):
    # code to check if '0.webp' exists on the AWS S3 bucket and
    # exit loop if it does.
    # If it doesn't exist yet, wait 2 seconds before retrying.
    print(
        f"Checking if 0.webp exists in {BUCKET_NAME}",
        f"s3 bucket on attempt {i}:",
    )
    for obj in client.list_objects(Bucket=BUCKET_NAME)["Contents"]:
        print(
            "Discover object {} on '{}' s3 bucket".format(
                obj["Key"],
                BUCKET_NAME,
            )
        )
        webp_list.append(obj["Key"])
    if "0.webp" in webp_list:
        print("Successflly 0.jpg converted to 0.webp.")
        break
    time.sleep(2)

assert "0.jpg" in webp_list
