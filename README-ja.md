# Image Converter on AWS Lambda

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## イントロダクション

このプロジェクトは、CloudFormation を使用して、アップロードされた画像を WebP 形式に自動的に変換する Lambda 関数とそれに付属する AWS リソースを提供します。本プロジェクトの CloudFormation テンプレートは、以下のリソースをプロビジョニングします。:

- アップロードされた画像を保存するための ImageStorageS3Bucket という名前の S3 バケット。
- ImageConverterLambdaFunction という名前の Lambda 関数。この関数は、画像が ImageStorageS3Bucket バケットにアップロードされると、S3 イベントによってトリガーされます。この関数は、アップロードされた画像を PIL を使って WebP 形式に変換し、ImageStorageS3Bucket バケットのアップロードされた画像と同じディレクトリに保存します。
- LambdaCodeS3Bucket という S3 バケット。ImageConverterLambdaFunction の Lambda 関数コードを格納するために使用されます。

## 必須ソフトウェア

- docker
- docker-compose
- vscode
- dev-contaner
- aws-cli (deploy スクリプトをホスト OS で実行する場合)
- pip (deploy スクリプトをホスト OS で実行する場合)

## localstack に対するデプロイ

devcontainer 内で実行して下さい。

```
make deploy_local
```

## localstack を用いた E2ETest

devcontainer 内で実行して下さい。

```
make e2e_test_local
```

## AWS 実環境に対するデプロイ

ホスト OS で実行して下さい。

```
make deploy_prod
```

## 開発

1. 以下のコードを実行して、vscode を起動して下さい。

   ```
   git clone https://github.com/NaGaii1994/ImageConverterOnAWSLambda
   cd ImageConverterOnAWSLambda
   code .
   ```

2. vscode が起動したら、Reopen container を選択して、devcontainer 内で開発して下さい。

## ユニットテスト

ImageConverterLambdaFunction 内で実行される python コードをテストします。
`make test`

## Licence

Copyright (c) 2023 NaGaii1994
ライセンスは MIT ライセンスとします。License を参照して下さい。
