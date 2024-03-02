import pandas as pd
import numpy
from sklearn.linear_model import LogisticRegression
import joblib

columns = joblib.load('columns.joblib')
log_model = joblib.load('log_model.joblib')
team_dict = joblib.load('teams.joblib')
stadium_dict = joblib.load('stadiums.joblib')


def stadium_names() -> list:
    return list(stadium_dict)


def team_names() -> list:
    return list(team_dict)


def predict(team1: str, team2: str, stadium: str, tosswinner: str, toss_des: int):
    datar = {col: 0 for col in columns}
    datar[f'TossWinner{tosswinner}'] = 1
    datar[f'TossDecision'] = toss_des
    datar[f'Team_{team1}'] = 1
    datar[f'Team_{team2}'] = 1
    datar[f'Venue_{stadium}'] = 1
    dataf = pd.DataFrame(datar, index=[0])
    xr = log_model.predict_proba(dataf)
    teams = list(team_dict)
    teams.sort()
    return {'team1': xr[0][teams.index(team1)], 'team2': xr[0][teams.index(team2)]}
