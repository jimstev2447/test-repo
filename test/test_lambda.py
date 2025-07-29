import json
import pytest
import os
import boto3
from moto import mock_aws

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
        yield boto3.client("s3", region_name="eu-west-1")


@pytest.fixture
def bucket(s3):
    s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    with open("test/data/test_file.txt") as f:
        text_to_write = f.read()
        s3.put_object(
            Body=text_to_write, Bucket="test_bucket", Key="sample/test_file.txt"
        )


def test_lambda_handler_logs_correct_text(valid_event, s3, bucket):
    lambda_handler(valid_event)
    assert False
