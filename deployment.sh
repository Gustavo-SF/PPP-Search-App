#!/bin/bash
#
# Deployment of Flask App

sed_primary_endpoint_key=$(echo $PRIMARY_ENDPOINT_KEY | sed 's/&/\\\&/g;s/\//\\\//g')
sed_scoring_uri=$(echo $SCORING_URI | sed 's/&/\\\&/g;s/\//\\\//g')

# Create the .env file for deploying to the server
sed "s/FLASK_SECRET/${SECRET_KEY}/; \
    s/MAIL_PLACEHOLDER/${MAIL_USERNAME}/; \
    s/MAIL_PWD_PLACEHOLDER/${MAIL_PASSWORD}/; \
    s/AZURE_DB_PLACEHOLDER/$DATABASE/; \
    s/AZURE_SERVER_PLACEHOLDER/${SERVER_NAME}/; \
    s/AZURE_USER_PLACEHOLDER/${LOGIN_INPUT}/; \
    s/AZURE_PWD_PLACEHOLDER/${PASSWORD_INPUT}/; \
    s/AZURE_SURI_PLACEHOLDER/${sed_scoring_uri}/; \
    s/AZURE_EKEY_PLACEHOLDER/${sed_primary_endpoint_key}/;" .env_template > .env