# Image Converter on AWS Lambda

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## イントロダクション
このプロジェクトは、CloudFormationを使用して、アップロードされた画像をWebP形式に自動的に変換するLambda関数とそれに付属するAWSリソースを提供します。本プロジェクトのCloudFormationテンプレートは、以下のリソースをプロビジョニングします。:

 - アップロードされた画像を保存するためのImageStorageS3Bucketという名前のS3バケット。
 - ImageConverterLambdaFunctionという名前のLambda関数。この関数は、画像がImageStorageS3Bucketバケットにアップロードされると、S3イベントによってトリガーされます。この関数は、アップロードされた画像をPILを使ってWebP形式に変換し、ImageStorageS3Bucketバケットのアップロードされた画像と同じディレクトリに保存します。
 - LambdaCodeS3BucketというS3バケット。ImageConverterLambdaFunctionのLambda関数コードを格納するために使用されます。


## 必須ソフトウェア

 - docker
 - docker-compose
 - vscode
 - dev-contaner
 - aws-cli (deployスクリプトをホストOSで実行する場合)
 - pip (deployスクリプトをホストOSで実行する場合)


## AWS実環境におけるデプロイ
ホストOSで実行して下さい。
```
make deploy
```

## 開発
1. 以下のコードを実行して、vscodeを起動して下さい。

    ```
    git clone https://github.com/NaGaii1994/ImageConverterOnAWSLambda
    cd ImageConverterOnAWSLambda
    code .
    ```
2. vscodeが起動したら、Reopen containerを選択して、devcontainer内で開発して下さい。

## Test
ImageConverterLambdaFunction内で実行されるpythonコードをテストします。
    ```
    make test
    ```

## Licence

Copyright (c) 2023 NaGaii1994
ライセンスはMITライセンスとします。Licenseを参照して下さい。
