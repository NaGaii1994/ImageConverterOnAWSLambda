#!/bin/bash

set -eu

source ./config

aws s3 rm s3://${AppName}-lambda-code-s3-bucket --recursive
aws s3 rm s3://${AppName}-image-storage-s3-bucket --recursive

aws cloudformation delete-stack \
    --stack-name ${StackNameOfLambdaCodeS3Bucket}


aws cloudformation delete-stack \
    --stack-name ${StackNameOfLambdaCode}

aws cloudformation delete-stack \
    --stack-name ${StackNameOfFrontendIAMUser}
