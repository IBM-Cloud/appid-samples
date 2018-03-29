#!/usr/bin/env bash

TARGET_INSTANCE = $1
REGION = $2
region = $REGION

if [ $REGION == "us-south" ]; then
    region = "ng"
fi

bx api api.$region.bluemix.net
bx login
bx resource service-instance-create $TARGET_INSTANCE appid graduated-tier $REGION

bx iam service-id-create appid-c -d "cloning test"
bx iam service-api-key-create appidc-key appid-c -d "appidc test key"
bx iam service-policy-create appid-c -r Reader --service-name appid --service-instance c8295e26-bd7a-4b58-ae85-d3775691a00e
bx iam service-policy-create appid-c -r Writer --service-name appid --service-instance 81b59d43-be0d-439c-971f-7b76f3c4f4e7