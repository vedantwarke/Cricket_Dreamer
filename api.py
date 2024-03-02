from flask import Flask, jsonify, request
from ibmwatson import *
from predicitor import *
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/api/get_players', methods=['GET'])
def get_players():
    if request.method == 'GET':
        return jsonify({'players': list(get_player_list())})


@app.route('/api/get_teams', methods=['GET'])
def get_teams():
    if request.method == 'GET':
        return jsonify({'teams': list(team_names())})


@app.route('/api/get_stadiums', methods=['GET'])
def get_stadiums():
    if request.method == 'GET':
        return jsonify({'stadiums': stadium_names()})


@app.route('/api/cities', methods=['GET'])
def get_cities():
    if request.method == 'GET':
        return jsonify({'cities': list({i for i in get_city_list() if i == i})})


@app.route('/api/winpredictor', methods=['POST'])
def predict_winner():
    if request.method == 'POST':
        args = request.get_json()
        team1 = args['team1']
        team2 = args['team2']
        stadium = args['stadium']
        tosswinner = args['tosswinner']
        toss_des = args['toss_des']
        return jsonify(predict(team1, team2, stadium, tosswinner, toss_des))


@app.route('/api/predictor', methods=['POST'])
def predict_players():
    if request.method == "POST":
        args = request.get_json()
        team_1 = args['team1']
        team_2 = args['team2']
        best_batter = batter_sorted(team_1+team_2, args['location'])
        best_bowler = bowler_sorted(team_1+team_2, args['location'])
        batter_list = best_batter.to_dict()['batsman_run']
        bowler_list = best_bowler.to_dict()['batsman_run']

        temp1 = sorted(batter_list.items(), key=lambda x: x[1], reverse=True)
        temp2 = sorted(bowler_list.items(), key=lambda x: x[1])

        x = {i: j for i, j in temp1}
        y = {i: j for i, j in temp2}

        dream11 = {}
        try:
            dream11['wicketkeeper'] = team_1[-1] if batter_list[team_1[-1]
                                                                ] > batter_list[team_2[-1]] else team_2[-1]
            dream11['allrounder1'] = team_1[-2] if batter_list[team_1[-2]
                                                               ] > batter_list[team_2[-2]] else team_2[-2]
            dream11['allrounder2'] = team_1[-3] if batter_list[team_1[-3]
                                                               ] > batter_list[team_2[-3]] else team_2[-3]

            batters = [dream11['wicketkeeper'],
                       dream11['allrounder1'], dream11['allrounder2']]
            bowlers = [dream11['wicketkeeper'],
                       dream11['allrounder1'], dream11['allrounder2']]
            for i in range(11):
                if len(batters) == 7:
                    break
                if list(x.keys())[i] not in bowlers:
                    batters.append(list(x.keys())[i])
                    dream11['batsman'+str(i+1)] = list(x.keys())[i]
            for i in range(11):
                if len(bowlers) == 7:
                    break
                if list(y.keys())[i] not in batters:
                    bowlers.append(list(y.keys())[i])
                    dream11['bowler'+str(i+1)] = list(y.keys())[i]
        except Exception as masg:
            return jsonify({"message": f"{masg} has not played in {args['location']}. Hence Not able to make a team"})

        return jsonify({"dream": dream11})


app.run(debug=True)
