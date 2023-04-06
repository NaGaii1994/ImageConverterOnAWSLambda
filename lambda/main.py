import io
import os
import urllib.parse

import boto3
from PIL import Image, UnidentifiedImageError

# バケット名,オブジェクト名
BUCKET_NAME = "s3-bucket-for-image-upload"

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    convert_image_to_webp(key)


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


def convert_image_to_webp(key):
    # Detect extension
    ext = os.path.splitext(key)[1][1:]

    if ext in ["jpg", "jpeg", "gif", "png"]:
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        image_data = io.BytesIO(s3_object["Body"].read())
        try:
            pil_image = Image.open(image_data)

            # Save to memory
            buffer = io.BytesIO()
            pil_image.save(buffer, "WebP")

            new_key = os.path.splitext(key)[0] + ".webp"

            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=new_key,
                Body=buffer.getvalue(),
            )

        except UnidentifiedImageError:
            print(f"{BUCKET_NAME}:{key} is not image file. It may be broken.")
            return None
