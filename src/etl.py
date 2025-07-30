import boto3
import csv
import json
import os


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


class Teams():
    def __init__(self, People):
        self._people = People()
        self._teams = []

    def update(self, headers, line):
        member = line[0]
        team = line[1]
        fav_snack = line[2]
        ate_times = line[3]
        sugar = line[4]

        formatted_team = team.lower()
        total_sugar = int(ate_times) * int(sugar)
        formatted_member = member.lower()

        existing_team_names = [team['name'] for team in self._teams]

        self._people.add_person(name=member, fav_snack=fav_snack)

        if formatted_team in existing_team_names:
            team = self._teams[existing_team_names.index(formatted_team)]
            team['members'].append(formatted_member)
            team['total_sugar'] += total_sugar
            team['mean_sugar_intake'] = team['total_sugar'] / \
                len(team['members'])
        else:
            self._teams.append({
                'name': formatted_team,
                'members': [formatted_member],
                'mean_sugar_intake': total_sugar,
                'total_sugar': total_sugar})

    def get_people(self):
        return self._people.get_people()

    def get_teams(self):
        return self._teams


class People():
    def __init__(self):
        self._people = []

    def add_person(self, name, fav_snack):
        formatted_name = name.lower()
        formatted_snack = fav_snack.lower()
        self._people.append(
            {'name': formatted_name, 'fav_snack': formatted_snack})

    def get_people(self):
        return self._people
