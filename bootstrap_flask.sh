#!/usr/bin/env bash
set -xe

APP_DIR=$PWD
TMP_DIR="/tmp/lambda-packages"
OUTPUT_ZIP="$PWD/flask-app.zip"
ARCHIVE_TMP="/tmp/lambda-bundle-tmp.zip"
SKIP_DEPENDANCIES=true

if [[ $1 = "--skip-deps" ]]
then
    SKIP_DEPENDANCIES=false
fi

# Clean TMP DIR
if [ $SKIP_DEPENDANCIES = true ]
then
    rm -rf $TMP_DIR
fi
rm $OUTPUT_ZIP || true
mkdir -p $TMP_DIR

# Copie App
cp -r * $TMP_DIR

# Install Dependancies
cd $TMP_DIR

# Clean App directory
rm run.sh
rm -rf venv

if [ $SKIP_DEPENDANCIES = true ]
then
    docker run --rm -it -v ${PWD}:/var/task lambci/lambda:build-python3.7 pip install -r requirements.txt --no-deps -t .
fi

# Package Lambda App
zip -q -r9 $OUTPUT_ZIP .

# Back to app dir
cd $APP_DIR

