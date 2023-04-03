import os

import boto3

# from main import list_backet_images
import main
import pytest
from boto3.s3.transfer import S3Transfer


@pytest.fixture
def setup():
    client = boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
    print("create s3 backet...")
    client.create_bucket(Bucket=main.BUCKET_NAME)
    transfer = S3Transfer(client)
    for i in range(5):
        transfer.upload_file(f"sample/{i}.jpg", main.BUCKET_NAME, f"{i}.jpg")

    yield client
    print("delete s3 backet...")
    for i in range(5):
        client.delete_object(Bucket=main.BUCKET_NAME, Key=f"{i}.jpg")
    client.delete_bucket(Bucket=main.BUCKET_NAME)


def test_list_backet_images(setup):
    main.s3_client = setup
    assert "0.jpg" in main.list_backet_images()
    assert "1.jpg" in main.list_backet_images()
    assert "2.jpg" in main.list_backet_images()
    assert "3.jpg" in main.list_backet_images()
    assert "4.jpg" in main.list_backet_images()


def test_convert_image_to_webp(setup):
    main.s3_client = setup

    main.convert_image_to_webp("0.jpg")
    webp = setup.get_object(Bucket=main.BUCKET_NAME, Key="0.webp")
    assert webp is not None
    setup.delete_object(Bucket=main.BUCKET_NAME, Key="0.webp")


def test_convert_image_to_webp_with_upload_webp_or_other_file(setup):
    main.s3_client = setup

    transfer = S3Transfer(setup)
    transfer.upload_file("sample/0.webp", main.BUCKET_NAME, "0.webp")

    result = main.convert_image_to_webp("0.webp")
    assert result is None
    setup.delete_object(Bucket=main.BUCKET_NAME, Key="0.webp")


def test_convert_image_to_webp_with_upload_broken_image_file(setup):
    main.s3_client = setup

    transfer = S3Transfer(setup)
    transfer.upload_file(
        "sample/broken_image.jpg",
        main.BUCKET_NAME,
        "broken_image.jpg",
    )

    result = main.convert_image_to_webp("broken_image.jpg")
    assert result is None
    setup.delete_object(Bucket=main.BUCKET_NAME, Key="broken_image.jpg")
