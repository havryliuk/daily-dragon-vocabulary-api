import json
import logging
import os
import secrets

import boto3
from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


def get_password_from_secrets():
    region_name = os.getenv("AWS_REGION", "us-west-2")
    secret_name = os.getenv("PASSWORD_SECRET_ID", "daily_dragon_password")
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logging.error(f"Error retrieving secret {secret_name}: {e}")
        raise e
    return get_secret_value_response["SecretString"]


def get_password():
    password = os.getenv("PASSWORD")
    if not password:
        print("No password provided in the .env file, fetching from AWS Secrets Manager.")
        secret_string = get_password_from_secrets()
        password = json.loads(secret_string)["SecretString"]
        print("Password retrieved from AWS Secrets Manager.")
    return password


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "havryliuk")
    password = get_password()
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
