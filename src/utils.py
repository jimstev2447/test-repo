

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
