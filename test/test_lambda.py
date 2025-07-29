import json
import pytest
import os
import boto3
from moto import mock_aws

import test_constants
from src.etl import lambda_handler

# TODO: valid event => successful file access => successful insert
# TODO: invalid event
#  TODO: unsuccessful file access
#  TODO: unsuccessful insert


@pytest.fixture
def valid_event():
    with open("test/data/s3_upload_event.json") as v:
        event = json.loads(v.read())
    return event


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def bucket(s3):
    s3.create_bucket(
        Bucket=test_constants.TEST_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    with open("test/data/test_file.txt") as f:
        text_to_write = f.read()
        s3.put_object(
            Body=text_to_write, Bucket=test_constants.TEST_BUCKET_NAME, Key=test_constants.TEST_OBJECT_KEY
        )


@pytest.fixture
def saved_bucket(s3):
    storage_bucket = s3.create_bucket(
        Bucket=test_constants.TEST_STORAGE_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    return storage_bucket


def test_lambda_handler_saves_to_bucket(valid_event, s3, bucket, saved_bucket):
    context = {}
    lambda_handler(valid_event, context=context)
    response = s3.get_object(Bucket=test_constants.TEST_STORAGE_BUCKET_NAME,
                             Key=test_constants.TEST_STORAGE_BUCKET_OBJECT_TARGET)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


def test_lambda_stores_correct_data(valid_event, s3, bucket, saved_bucket):
    context = {}
    lambda_handler(valid_event, context=context)
    response = s3.get_object(Bucket=test_constants.TEST_STORAGE_BUCKET_NAME,
                             Key=test_constants.TEST_STORAGE_BUCKET_OBJECT_TARGET)
    data = json.loads(response['Body'].read().decode('utf-8'))
    with open(file="./test/data/test_output.json")as file:
        expected_data = json.loads(file.read())
        assert expected_data == data
