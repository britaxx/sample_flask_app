#!/bin/bash 

export AWS_REGION='eu-west-1'
export S3_BUCKET='abrit-aws-serverless-photolibrary'

export AWS_COGNITO_USER_POOL_ID='eu-west-1_hHZ4h0PAG'
export AWS_COGNITO_USER_POOL_CLIENT_ID='7va52273h35ueg7oso6g7mb5jv'
export AWS_COGNITO_USER_POOL_CLIENT_SECRET='bi4n0o1dcpad2nc464lt2245f7hp1tv7ji6357p7ro3a3vr8mbc'
export AWS_COGNITO_REDIRECT_URL='http://localhost:5000/loggedin'
export AWS_COGNITO_DOMAIN='abrit-auth.auth.eu-west-1.amazoncognito.com'

export DYNAMO_TABLE_NAME='abrit-aws-serverless-photolibrary' 

export AWS_PROFILE='formation'

python handler.py