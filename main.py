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


def main():
    teams = read_teams()
    find_institutions(teams)


def read_teams():
    with open("2015.csv", "r") as file:
        return [row for row in csv.DictReader(file)]


def find_teams_by_ranking(teams, ranking):
    if ranking not in POSSIBLE_RANKINGS:
        raise ValueError("Invalid ranking")
    return [team for team in teams if team["Ranking"] == ranking]


def find_avg_teams_per_institution():
    pass


def find_institutions(teams):
    institutions = []
    for index, team in enumerate(teams):
        # print(index/len(teams) * 100)
        matching_institution = None

        for institution in institutions:
            if team["ï»¿Institution"] == institution:
                matching_institution = institution
            elif fuzz.ratio(team["ï»¿Institution"], institution) > 80 \
                    and fuzz.ratio(team["ï»¿Institution"].split(" ")[0], institution.split(" ")[0]) > 80:
                matching_institution = institution

        if matching_institution is None:
            institutions.append(team["ï»¿Institution"])

    institutions.sort()
    with open("institutions.txt", "w") as file:
        file.write(("\n").join(institutions))


if __name__ == "__main__":
    main()
