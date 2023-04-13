import os

import boto3

# from main import list_backet_images
import main
import pytest
from boto3.s3.transfer import S3Transfer


@pytest.fixture
def test_client():
    client = boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
    region_name = os.getenv("AWS_DEFAULT_REGION")
    print("create s3 backet...")
    main.BUCKET_NAME = "test-bucket"
    main.s3_client = client
    client.create_bucket(
        Bucket=main.BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": region_name},
    )
    transfer = S3Transfer(client)
    transfer.upload_file("sample/0.jpg", main.BUCKET_NAME, "0.jpg")

    yield client
    print("delete s3 backet...")
    client.delete_object(Bucket=main.BUCKET_NAME, Key="0.jpg")
    client.delete_bucket(Bucket=main.BUCKET_NAME)


def test_convert_image_to_webp(test_client):
    main.convert_image_to_webp("0.jpg")
    webp = test_client.get_object(Bucket=main.BUCKET_NAME, Key="0.webp")
    assert webp is not None
    test_client.delete_object(Bucket=main.BUCKET_NAME, Key="0.webp")


def test_convert_image_to_webp_with_upload_webp_or_other_file(test_client):
    transfer = S3Transfer(test_client)
    transfer.upload_file("sample/0.webp", main.BUCKET_NAME, "0.webp")

    result = main.convert_image_to_webp("0.webp")
    assert result is None
    test_client.delete_object(Bucket=main.BUCKET_NAME, Key="0.webp")


def test_convert_image_to_webp_with_upload_broken_image_file(test_client):
    transfer = S3Transfer(test_client)
    transfer.upload_file(
        "sample/broken_image.jpg",
        main.BUCKET_NAME,
        "broken_image.jpg",
    )

    result = main.convert_image_to_webp("broken_image.jpg")
    assert result is None
    test_client.delete_object(Bucket=main.BUCKET_NAME, Key="broken_image.jpg")
