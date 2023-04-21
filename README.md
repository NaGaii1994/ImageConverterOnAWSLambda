# Image Converter on AWS Lambda

[日本語版 README はこちら](https://github.com/NaGaii1994/ImageConverterOnAWSLambda/blob/main/README-ja.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

This App provisions the necessary AWS resources to enable automatic conversion of uploaded images to the WebP format by using CloudFormation. The CloudFormation template provisions the following resources:

- An S3 bucket named ImageStorageS3Bucket that is used to store uploaded images.
- A Lambda function named ImageConverterLambdaFunction is triggered by S3 events when an image is uploaded to the ImageStorageS3Bucket bucket. The function converts the uploaded image to the WebP format using PIL and stores it in the same directory as the uploaded image in the ImageStorageS3Bucket bucket.
- An S3 bucket named LambdaCodeS3Bucket that is used to store the Lambda function code.

## Requirements

- docker
- docker-compose
- vscode
- dev-contaner
- aws-cli (For execute deploy command on your host machine)
- pip (For execute deploy command on your host machine)

## Deploy

on your host machine(not on container)

```
make deploy
```

## Develop

1. Please excute this command.

   ```
   git clone https://github.com/NaGaii1994/ImageConverterOnAWSLambda
   cd ImageConverterOnAWSLambda
   code .
   ```

2. When open vscode, please select "Reopne in container".

## Test

Test the python code of the image converter using localstack.
`make test`

## Licence

Copyright (c) 2023 NaGaii1994
This software is released under the MIT License, see LICENSE.
