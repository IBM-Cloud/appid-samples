#!/usr/bin/env bash

TARGET_INSTANCE=$1
REGION=$2

SERVICE_ID_NAME=$TARGET_INSTANCE-configurator
region=$REGION

if [ $REGION == "us-south" ]; then
    region = "ng"
fi

bx api api.$region.bluemix.net
bx login
bx resource service-instance-create $TARGET_INSTANCE appid graduated-tier $REGION

bx iam service-id-create $SERVICE_ID_NAME -d "configurator task for $TARGET_INSTANCE"
bx iam service-api-key-create appidc-key $SERVICE_ID_NAME
bx iam service-policy-create $SERVICE_ID_NAME -r Reader --service-name appid
bx iam service-policy-create $SERVICE_ID_NAME -r Writer --service-name appid --service-instance $TARGET_INSTANCE

echo "App ID instance created:"
bx resource service-instance $TARGET_INSTANCE