import csv
from typing import Any
from collections import defaultdict


def read_file():
    directory = 'C:/Users/jacom/PycharmProjects/pythonProject'
    file_name = '693085.csv'
    f = open("{}/NTB/".format(directory) + "{}".format(file_name), "r")
    csv_f = list(csv.reader(f))
    f.close()
    return csv_f


def info_grabber(csv_f):
    info_list = []
    player_list = []
    registry = []
    info = {}
    team_sheet = {}
    player_registry = {}
    # Adding useful information from spreadsheet to lists
    for row in csv_f:
        useless_rows = ["version", "balls_per_over", "gender", "season", "event", "city"]
        if row[0] in useless_rows:
            continue
        elif row[0] == "info" and row[1] != "player" and row[1] != "registry":
            info_list.append([row[1], row[2]])
        elif row[0] == "info" and row[1] == "player":
            player_list.append([row[2], row[3]])
        elif row[0] == 'info' and row[1] == 'registry':
            registry.append([row[3], row[4]])
        else:
            break
    # Converting 2D lists to 1D lists
    info_listed = [val for sublist in info_list for val in sublist]
    players_listed = [val for sublist in player_list for val in sublist]
    registry_listed = [val for sublist in registry for val in sublist]
    # Creating dictionaries of match info
    for _ in csv_f:
        if _[1] == 'team' and 'home team' not in info:
            info["home team"] = _[2]
        elif _[1] == 'team':
            info["away team"] = _[2]
    for i in range(3, len(info_listed) - 1):
        if i % 2 == 0:
            info[info_listed[i]] = info_listed[i + 1]
    for i in range(len(players_listed) - 1):
        if i % 2 == 0:
            if players_listed[i] not in team_sheet:
                team_sheet[players_listed[i]] = players_listed[i + 1]
            elif players_listed[i] in team_sheet:
                team_sheet[players_listed[i]] += f", {players_listed[i + 1]}"
    for i in range(len(registry_listed) - 1):
        if i % 2 == 0:
            player_registry[registry_listed[i]] = registry_listed[i + 1]
    return info


def match_stats_grabber(csv_f, info: object):
    # column_headings = ["0 ball", "1 Innings", "2 Over", "3 Batting Team",
    # 4 On-Strike Batter", "5 Off-Strike Batter", "6 Bowler", "7 Runs",
    # 8 Extras", "9 Wides", "10 No-Ball", "11 Byes", "12 Leg-Byes",
    # 13 Penalty", "14 How out", "15 Player Out"]"""
    # Assigning variables
    first_innings_runs: dict[Any, int] = {}
    first_innings_scorecard = {}
    first_innings_balls = {}
    first_innings_how_out = {}
    first_innings_runs_dict = {}
    ball_count = 0
    second_innings_runs: dict[Any, int] = {}
    second_innings_scorecard = {}
    second_innings_balls = {}
    second_innings_how_out = {}
    second_innings_runs_dict = {}
    team_total = {}

    # overs_bowled = {}
    # runs_conceded = {}
    # bowling = {}
    # wickets = {}
    # bowling_figures = {'bowler': 0, overs_bowled, maidens, runs_conceded, wickets, wides, no-first_innings_balls}
    # Determining who lost the toss and who is batting first
    if info['home team'] == info['toss_winner']:
        toss_loser = info['away team']
    elif info['home team'] != info['toss_winner']:
        toss_loser = info['home team']
    if info['toss_decision'] == 'field':
        first_innings: object = toss_loser
    elif info['toss_decision'] != 'field':
        first_innings = info['toss_winner']
    # Determining which team the extras belong to for each innings
    if first_innings == info['toss_winner']:
        first_innings_extras = {'bowling team': f"{toss_loser}", 'total': 0, 'wides': 0, 'no-balls': 0,
                                'byes': 0, 'leg-byes': 0, 'penalty': 0}
        second_innings_extras = {'bowling team': f"{info['toss_winner']}", 'total': 0, 'wides': 0,
                                 'no-balls': 0, 'byes': 0, 'leg-byes': 0, 'penalty': 0}
    elif first_innings != info['toss_winner']:
        first_innings_extras = {'bowling team': f"{info['toss_winner']}", 'total': 0, 'wides': 0,
                                'no-balls': 0, 'byes': 0, 'leg-byes': 0, 'penalty': 0}
        second_innings_extras = {'bowling team': f"{toss_loser}", 'total': 0, 'wides': 0, 'no-balls': 0,
                                 'byes': 0, 'leg-byes': 0, 'penalty': 0}
    for row in csv_f:
        if row[0] == "info" or row[0] == "version":
            continue
        elif row[0] != "ball":
            break
        else:
            batter = row[4]
            team = row[3]
            # Summing how much each team scored
            if team not in team_total:
                team_total[team] = int(row[7]) + int(row[8])
            elif team in team_total:
                team_total[team] += int(row[7]) + int(row[8])
            # Summing how much each batter scored and creating scorecard for their innings
            if int(row[1]) == 1:
                ball_count += 1
                if batter not in first_innings_runs:
                    first_innings_runs[batter] = int(row[7])
                    first_innings_scorecard[batter] = "{}".format(row[7])
                elif batter in first_innings_runs:
                    first_innings_runs[batter] += int(row[7])
                    first_innings_scorecard[batter] += "{}".format(row[7])
                else:
                    print("Error in adding {}'s total".format(batter))
                # if not a wide, start counting deliveries
                if row[9] == "":
                    if batter not in first_innings_balls:
                        first_innings_balls[batter] = 1
                    elif batter in first_innings_balls:
                        first_innings_balls[batter] += 1
                elif batter not in first_innings_balls:
                    first_innings_balls[batter] = 0
                if row[15] != "":
                    first_innings_how_out[batter] = row[14]
            # Second innings additions
            elif int(row[1]) == 2:
                ball_count += 1
                if batter not in second_innings_runs:
                    second_innings_runs[batter] = int(row[7])
                    second_innings_scorecard[batter] = "{}".format(row[7])
                elif batter in second_innings_runs:
                    second_innings_runs[batter] += int(row[7])
                    second_innings_scorecard[batter] += "{}".format(row[7])
                else:
                    print("Error in adding {}'s total".format(batter))
                # if not a wide, start counting deliveries
                if row[9] == "":
                    if batter not in second_innings_balls:
                        second_innings_balls[batter] = 1
                    elif batter in second_innings_balls:
                        second_innings_balls[batter] += 1
                elif batter not in second_innings_balls:
                    second_innings_balls[batter] = 0
                if row[15] != "":
                    second_innings_how_out[batter] = row[14]
            # Extras calculations for the first innings
            if int(row[1]) == 1 and int(row[8]) != 0:
                first_innings_extras['total'] += int(float(row[8]))
                if row[9] != '':
                    first_innings_extras['wides'] += int(float(row[9]))
                elif row[10] != '':
                    first_innings_extras['no-balls'] += int(float(row[10]))
                elif row[11] != '':
                    first_innings_extras['byes'] += int(float(row[11]))
                elif row[12] != '':
                    first_innings_extras['leg-byes'] += int(float(row[12]))
                elif row[13] != '':
                    first_innings_extras['penalty'] += int(float(row[13]))
            # Assigning not outs to the batters at the end of the innings
            if ball_count == sum(first_innings_balls.values()) + first_innings_extras['wides'] and row[
                14] == '':
                first_innings_how_out[row[4]] = 'Not out'
                first_innings_how_out[row[5]] = 'Not out'
            elif ball_count == sum(first_innings_balls.values()) + first_innings_extras['wides'] and row[
                14] != '':
                if row[4] == row[15]:
                    first_innings_how_out[row[5]] = 'Not out'
                elif row[5] == row[15]:
                    first_innings_how_out[row[4]] = 'Not out'
            # Extras calculations for the second innings
            if row[1] == 2 and 0 != row[8]:
                second_innings_extras['total'] += int(float(row[8]))
                if row[9] != '':
                    second_innings_extras['wides'] += int(float(row[9]))
                elif row[10] != '':
                    second_innings_extras['no-balls'] += int(float(row[10]))
                elif row[11] != '':
                    second_innings_extras['byes'] += int(float(row[11]))
                elif row[12] != '':
                    second_innings_extras['leg-byes'] += int(float(row[12]))
                elif row[13] != '':
                    second_innings_extras['penalty'] += int(float(row[13]))
    # Assigning not outs to the batters at the end of the innings
    if team_total[first_innings] < list(team_total.values())[1]:
        second_innings_how_out[row[4]] = 'Not out'
        second_innings_how_out[row[5]] = 'Not out'
    elif team_total >= list(team_total.values())[1]:
        if row[5] == row[15]:
            second_innings_how_out[row[4]] = 'Not out'
        elif row[4] == row[15]:
            second_innings_how_out[row[5]] = 'Not out'
    # This loop adds creates a breakdown of how they scored their first_innings_runs and returns
    # an array with the batters name and the breakdown
    for batter_name, scores in first_innings_scorecard.items():
        listed_scores = sorted(list(scores))
        breakdown = [[score, listed_scores.count(score)] for score in set(listed_scores)]
        first_innings_runs_dict[batter_name] = sorted(breakdown)
    for batter_name, scores in second_innings_scorecard.items():
        listed_scores = sorted(list(scores))
        breakdown = [[score, listed_scores.count(score)] for score in set(listed_scores)]
        second_innings_runs_dict[batter_name] = sorted(breakdown)
    # Bowling figures
    # Determining match result
    if len(list(team_total.values())) == 2:
        if team_total[first_innings] > list(team_total.values())[1]:
            print(f"{info['home team']} won by {info['winner_runs']} first_innings_runs")
        elif team_total[first_innings] == list(team_total.values())[1]:
            print('Tie')
        elif team_total[first_innings] < list(team_total.values())[1]:
            print(f"{info['home team']} won by {info['winner_wickets']} wickets")
    else:
        print("No Result")

    # first_innings_batting_card = defaultdict(list)
    # first_innings_batting_card = {'balls': first_innings_balls}

    # get keys from one of the dictionary
    # ks = [k for k in first_innings_runs.keys()]

    # call values from each dictionary on available keys
    # first_d_merged = {k: (first_innings_runs[k], first_innings_balls[k], first_innings_runs_dict[k]) for k in ks}

    # for d in (first_innings_runs, first_innings_balls, first_innings_runs_dict, first_innings_how_out):
    #     for key, value in d.items():
    #         first_innings_batting_card[key].append(value)

    # print(first_d_merged)
    #
    print(first_innings_runs)
    print(second_innings_runs)
    print(first_innings_balls)
    print(second_innings_balls)
    print(first_innings_how_out)
    print(second_innings_how_out)
    print(first_innings_runs_dict)
    print(second_innings_runs_dict)
    return


def build_file():
    print("hello world")


if __name__ == "__main__":
    x = read_file()
    y = info_grabber(x)
    (match_stats_grabber(x, y))
