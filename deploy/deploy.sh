#!/bin/bash

set -eu

source ./config

NameOfLambdaCodeS3Bucket="s3-bucket-for-lambda-deploy"

NameOfImageStorageS3Bucket="s3-bucket-for-image-upload"
NameOfImageConverterLambdaFunction="image-converter-lambda"

EnvironmentType="ci"

# テンプレートの実行
aws cloudformation deploy \
    --stack-name ${StackNameOfLambdaCodeS3Bucket} \
    --template-file ./cloudformation/s3_bucket_for_image_converter_code.yml \
    --parameter-overrides \
    NameOfLambdaCodeS3Bucket=${NameOfLambdaCodeS3Bucket}

cp -r ../lambda bootstrap
pip install --requirement ./bootstrap/requirements/prod.txt \
    --platform manylinux2014_x86_64 \
    --target=./bootstrap \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade
rm -r -f ./bootstrap/sample ./bootstrap/requirements
cd bootstrap && zip -r ../bootstrap.zip .
cd ..
rm -r -f ./bootstrap

aws s3 mv \
    ./bootstrap.zip \
    s3://${NameOfLambdaCodeS3Bucket}/bootstrap.zip

aws cloudformation deploy \
    --stack-name ${StackNameOfLambdaCode} \
    --template-file ./cloudformation/image_converter.yml \
    --parameter-overrides \
    NameOfLambdaCodeS3Bucket=${NameOfLambdaCodeS3Bucket} \
    NameOfImageStorageS3Bucket=${NameOfImageStorageS3Bucket} \
    NameOfImageConverterLambdaFunction=${NameOfImageConverterLambdaFunction} \
    EnvironmentType=${EnvironmentType} \
    --capabilities CAPABILITY_NAMED_IAM
