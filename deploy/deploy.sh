#!/bin/bash

set -eu

source ./config

if [ $# -ne 1 ]
then
    echo "Usage: $0 local|ci|prod"
    exit 1
fi

EnvironmentType=$1

case $1 in
    "local")
        # テンプレートの実行
        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCodeS3Bucket} \
            --template-file ./cloudformation/s3_bucket_for_image_converter_code.yml \
            --parameter-overrides \
            AppName=${AppName} \
            --endpoint-url=http://localstack:4566
        ;;
    "ci")
        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCodeS3Bucket} \
            --template-file ./cloudformation/s3_bucket_for_image_converter_code.yml \
            --parameter-overrides \
            AppName=${AppName} \
            --endpoint-url=http://localhost:4566
        ;;
    "prod")
        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCodeS3Bucket} \
            --template-file ./cloudformation/s3_bucket_for_image_converter_code.yml \
            --parameter-overrides \
            AppName=${AppName}
        ;;
esac
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

case $1 in
    "local")
        aws s3 mv \
            ./bootstrap.zip \
            s3://${AppName}-lambda-code-s3-bucket/bootstrap.zip \
            --endpoint-url=http://localstack:4566

        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCode} \
            --template-file ./cloudformation/image_converter.yml \
            --parameter-overrides \
            AppName=${AppName} \
            EnvironmentType=${EnvironmentType} \
            --capabilities CAPABILITY_NAMED_IAM \
            --endpoint-url=http://localstack:4566
            ;;
    "ci")
        aws s3 mv \
            ./bootstrap.zip \
            s3://${AppName}-lambda-code-s3-bucket/bootstrap.zip \
            --endpoint-url=http://localhost:4566

        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCode} \
            --template-file ./cloudformation/image_converter.yml \
            --parameter-overrides \
            AppName=${AppName} \
            EnvironmentType=${EnvironmentType} \
            --capabilities CAPABILITY_NAMED_IAM \
            --endpoint-url=http://localhost:4566
            ;;
    "prod")
        aws s3 mv \
            ./bootstrap.zip \
            s3://${AppName}-lambda-code-s3-bucket/bootstrap.zip

        aws cloudformation deploy \
            --stack-name ${StackNameOfLambdaCode} \
            --template-file ./cloudformation/image_converter.yml \
            --parameter-overrides \
            AppName=${AppName} \
            EnvironmentType=${EnvironmentType} \
            --capabilities CAPABILITY_NAMED_IAM
esac
