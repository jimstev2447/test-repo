from src.utils import Teams, People


class Test_People():
    def test_get_people_returns_list(self):
        people = People()
        assert people.get_people() == []

    def test_add_people_adds_data_to_list(self):
        people = People()
        people.add_person("Alice", "Chocolate")
        assert len(people.get_people()) == 1

    def test_name_and_snack_added(self):
        people = People()
        people.add_person("alice", "chocolate")
        person = people.get_people()[0]
        assert person['name'] == 'alice'
        assert person['fav_snack'] == 'chocolate'

    def test_name_and_snack_formatted(self):
        people = People()
        people.add_person("ALIcE", "ChocOlaTe")
        person = people.get_people()[0]
        assert person['name'] == 'alice'
        assert person['fav_snack'] == 'chocolate'

    def test_add_people_adds_multiple(self):
        people = People()
        people.add_person("test_1", "test_snack_1")
        people.add_person("test_2", "test_snack_2")
        assert len(people.get_people()) == 2


class Test_Teams():
    def test_get_teams_returns_list(self):
        teams = Teams(People)
        assert teams.get_teams() == []

    def test_update_adds_team(self):
        teams = Teams(People)
        headers = ['name', 'team', 'favourite_snack',
                   'times_per_week', 'sugar_grams']
        line = ['Alice', 'Engineering', 'Chocolate', '5', '20']
        teams.update(headers=headers, line=line)
        assert len(teams.get_teams()) == 1
        assert len(teams.get_people()) == 1
        assert teams.get_people() == [
            {'name': 'alice', 'fav_snack': "chocolate"}]
        assert teams.get_teams()[0]['name'] == 'engineering'
        assert teams.get_teams()[0]['members'] == ["alice"]
        assert teams.get_teams()[0]['mean_sugar_intake'] == 100

    def test_update_adds_to_existing_team(self):
        teams = Teams(People)
        headers = ['name', 'team', 'favourite_snack',
                   'times_per_week', 'sugar_grams']
        line = ['Alice', 'Engineering', 'Chocolate', '5', '20']
        line_2 = ['Diana', 'Engineering', 'Popcorn', '2', '8']
        teams.update(headers=headers, line=line)
        teams.update(headers=headers, line=line_2)
        assert len(teams.get_teams()) == 1
        assert len(teams.get_teams()[0]['members']) == 2

    def test_updates_mean_sugar(self):
        teams = Teams(People)
        headers = ['name', 'team', 'favourite_snack',
                   'times_per_week', 'sugar_grams']
        line = ['Alice', 'Engineering', 'Chocolate', '5', '20']
        line_2 = ['Diana', 'Engineering', 'Popcorn', '2', '8']
        teams.update(headers=headers, line=line)
        teams.update(headers=headers, line=line_2)
        team = teams.get_teams()[0]
        assert team['mean_sugar_intake'] == ((100 + 16) / 2)
