import io
import os
import urllib.parse

import boto3
from PIL import Image, UnidentifiedImageError

# バケット名,オブジェクト名
BUCKET_NAME = os.getenv("IMAGE_STORAGE_S3_BUCKET")

s3_client = boto3.client("s3")
if os.getenv("AWS_ENDPOINT_URL"):
    print("aws endpoint is {}".format(os.getenv("AWS_ENDPOINT_URL")))
    s3_client = boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    convert_image_to_webp(key)


def convert_image_to_webp(key):
    # Detect extension
    ext = os.path.splitext(key)[1][1:]
    print(f"converting {key} to webp...")

    if ext in [
        "jpg",
        "JPG",
        "jpeg",
        "JPEG",
        "gif",
        "GIF",
        "png",
        "PNG",
        "bmp",
        "BMP",
    ]:
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        image_data = io.BytesIO(s3_object["Body"].read())
        try:
            pil_image = Image.open(image_data)

            # Save to memory
            buffer = io.BytesIO()
            pil_image.save(buffer, "WebP")

            new_key = os.path.splitext(key)[0] + ".webp"

            print(f"Uploading {new_key} to S3 Bucket {BUCKET_NAME}...")
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=new_key,
                Body=buffer.getvalue(),
            )

        except UnidentifiedImageError:
            print(f"{BUCKET_NAME}:{key} is not image file. It may be broken.")
            return None
