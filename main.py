import csv
from thefuzz import fuzz

POSSIBLE_RANKINGS = [
    "Meritorious",
    "Honorable Mention",
    "Successful Participant",
    "Finalist",
    "Outstanding Winner",
    "Unsuccessful"
]


class Institution:
    """
    Simple class to represent an institution.
    """

    def __init__(self, id, name, city, state, country):
        self.id: int = id
        self.names: list = [name]
        self.best_name: str = name
        self.teams: list = []
        self.city: str = city
        self.state: str = state
        self.country: str = country
        self.flagged_for_deletion = False

    def update_best_name(self):
        """
        Guess "real" institution name is most common name.
        """
        self.best_name = max(set(self.names), key=self.names.count)

    def add_team(self, team):
        self.teams.append(team)

    def merge(self, other):
        if self is other:
            # Refuse to merge with self
            return
        self.names += other.names
        self.teams += other.teams
        for team in other.teams:
            team.institution = self
        self.update_best_name()
        other.flagged_for_deletion = True

    def add_name(self, name):
        self.names.append(name)
        self.update_best_name()


class Team:
    """
    Simple class to represent a team.
    """

    def __init__(self, team_number, advisor, problem, ranking):
        self.team_number: int = team_number
        self.advisor: str = advisor
        self.problem: str = problem
        self.ranking: str = ranking
        self.institution: int = None


def main():
    teams, institutions = read_teams_and_institutions()
    institutions = deduplicate_institutions(institutions)
    for institution in institutions:
        print(institution.names)


def read_teams_and_institutions():
    with open("2015.csv", "r") as file:
        rows = csv.DictReader(file)
        teams = []
        institutions = []
        for row in rows:
            team = Team(
                team_number=row["Team Number"],
                advisor=row["Advisor"],
                problem=row["Problem"],
                ranking=row["Ranking"],
            )
            institution = Institution(
                id=len(institutions),
                name=row["ï»¿Institution"],
                city=row["City"],
                state=row["State/Province"],
                country=row["Country"]
            )

            institution.add_team(team)
            team.institution = institution
            institutions.append(institution)
            teams.append(team)
    return teams, institutions


def find_teams_by_ranking(teams, ranking):
    if ranking not in POSSIBLE_RANKINGS:
        raise ValueError("Invalid ranking")
    return [team for team in teams if team["Ranking"] == ranking]


def find_avg_teams_per_institution():
    pass


def make_minimal_name(name):
    # Remove all the extra stuff
    # Because "Montana State University" and "Michigan State University" are
    # more similar than "Montana" and "Michigan"
    minimal_name = name
    minimal_name = minimal_name.strip().lower()
    minimal_name = minimal_name.replace("of", "")
    minimal_name = minimal_name.replace("university", "")
    minimal_name = minimal_name.replace("college", "")
    minimal_name = minimal_name.replace("school", "")
    minimal_name = minimal_name.replace("and", "")
    minimal_name = minimal_name.replace("institute", "")
    minimal_name = minimal_name.replace("  ", " ")
    minimal_name = minimal_name.replace(",", "")
    return minimal_name


def make_acronym(full_name):
    words = full_name.split(" ")
    acronym = "".join([word[0] for word in words])
    return acronym


def deduplicate_institutions(institutions):
    for index, current_institution in enumerate(institutions):
        print(index, index/len(institutions) * 100, "%")
        if len(current_institution.names) != 1:
            continue

        if current_institution.flagged_for_deletion:
            continue

        current_min_name = make_minimal_name(
            current_institution.best_name)
        current_acronym = make_acronym(current_institution.best_name)
        for institution_match_candidate in institutions:
            if institution_match_candidate.flagged_for_deletion:
                continue
            candidate_min_name = make_minimal_name(
                institution_match_candidate.best_name)
            candidate_acronym = make_acronym(
                institution_match_candidate.best_name)
            if current_min_name == candidate_min_name:
                institution_match_candidate.merge(current_institution)
                break
            elif fuzz.ratio(current_min_name, candidate_min_name) > 90:
                institution_match_candidate.merge(current_institution)
                break
            elif len(current_institution.best_name) < 5 or len(institution_match_candidate.best_name) < 5:
                if fuzz.ratio(current_institution.best_name, candidate_acronym) > 90 \
                        or fuzz.ratio(current_acronym, institution_match_candidate.best_name) > 90:
                    institution_match_candidate.merge(current_institution)
                    print(current_institution.best_name, "|",
                          institution_match_candidate.best_name)
                    input()
                    break
        filtered_institutions = []
        for institution in institutions:
            if not institution.flagged_for_deletion:
                filtered_institutions.append(institution)
        institutions = filtered_institutions

    filtered_institutions.sort(key=lambda institution: institution.best_name)
    with open("institutions.txt", "w") as file:
        file.write(("\n").join(
            [institution.best_name for institution in institutions]))
    return filtered_institutions


if __name__ == "__main__":
    main()
