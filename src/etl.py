import boto3
import csv
import json
import os

from src.utils import People, Teams


def lambda_handler(event, context):
    STORAGE_BUCKET_NAME = os.environ['STORAGE_BUCKET_NAME']
    s3_bucket_name = event['Records'][0]["s3"]["bucket"]["name"]
    s3_object_name = event['Records'][0]["s3"]["object"]["key"]
    file_title = s3_object_name.replace(".txt", ".json")
    s3 = boto3.client("s3")
    data = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_name)

    contents = data["Body"].read().decode('utf-8')
    csv_items = list(csv.reader(contents.splitlines(), delimiter=","))
    headers = csv_items.pop(0)
    teams = Teams(People=People)
    for line in csv_items:
        teams.update(line=line, headers=headers)

    to_store = {
        "teams": teams.get_teams(),
        "people": teams.get_people()
    }

    s3.put_object(Body=json.dumps(to_store),
                  Bucket=STORAGE_BUCKET_NAME, Key=file_title)
    pass
