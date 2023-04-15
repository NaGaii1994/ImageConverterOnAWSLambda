#!/bin/bash

set -eu

source ./config

NameOfLambdaCodeS3Bucket="s3-bucket-for-lambda-deploy"
NameOfImageStorageS3Bucket="s3-bucket-for-image-upload"

aws s3 rm s3://${NameOfLambdaCodeS3Bucket} --recursive
aws s3 rm s3://${NameOfImageStorageS3Bucket} --recursive

aws cloudformation delete-stack \
    --stack-name ${StackNameOfLambdaCodeS3Bucket}


aws cloudformation delete-stack \
    --stack-name ${StackNameOfLambdaCode}
