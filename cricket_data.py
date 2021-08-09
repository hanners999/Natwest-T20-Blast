import csv
from typing import Any


def read_file():
    directory = 'C:/Users/jacom/PycharmProjects/pythonProject'
    file_name = '693009.csv'
    f = open(f'{directory}/NTB/' + f'{file_name}', 'r')
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
        useless_rows = ['version', 'balls_per_over', 'gender', 'season', 'event', 'city']
        if row[0] in useless_rows:
            continue
        elif row[0] == 'info' and row[1] != 'player' and row[1] != 'registry':
            info_list.append([row[1], row[2]])
        elif row[0] == 'info' and row[1] == 'player':
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
            info['home team'] = _[2]
        elif _[1] == 'team':
            info['away team'] = _[2]
    for i in range(3, len(info_listed) - 1):
        if i % 2 == 0:
            info[info_listed[i]] = info_listed[i + 1]
    for i in range(len(players_listed) - 1):
        if i % 2 == 0:
            if players_listed[i] not in team_sheet:
                team_sheet[players_listed[i]] = players_listed[i + 1]
            else:
                team_sheet[players_listed[i]] += f', {players_listed[i + 1]}'
    for i in range(len(registry_listed) - 1):
        if i % 2 == 0:
            player_registry[registry_listed[i]] = registry_listed[i + 1]
    return info, team_sheet


def match_stats_grabber(csv_f, info, team_sheet):
    # Assigning variables
    first_innings_runs: dict[Any, int] = {}
    first_innings_scorecard = {}
    first_innings_balls = {}
    first_innings_how_out = {}
    first_innings_runs_dict = {}
    first_innings_batting_card = {}
    ball_count = 0
    second_innings_runs: dict[Any, int] = {}
    second_innings_scorecard = {}
    second_innings_balls = {}
    second_innings_how_out = {}
    second_innings_runs_dict = {}
    second_innings_batting_card = {}
    team_total = {}
    home_team = info['home team']
    first_innings_balls_bowled = {}
    first_innings_overs_bowled = {}
    first_innings_maidens = {}
    first_innings_runs_conceded = {}
    first_innings_wickets = {}
    first_innings_wickets['Run out'] = 0
    first_innings_wickets_type = {}
    first_innings_wickets_type['Run out'] = 0
    first_innings_bowling_scorecard = {}
    second_innings_balls_bowled = {}
    second_innings_overs_bowled = {}
    second_innings_maidens = {}
    second_innings_runs_conceded = {}
    second_innings_wickets = {}
    second_innings_wickets['Run out'] = 0
    second_innings_wickets_type = {}
    second_innings_wickets_type['Run out'] = 0
    # bowling_figures = {'bowler': 0, overs_bowled, maidens, runs_conceded, wickets, wides, no-first_innings_balls}
    # Determining who lost the toss and who is batting first
    toss_winner = info['toss_winner']
    toss_loser = info['away team' if (home_team == toss_winner) else 'home team']

    # Determining which team the extras belong to for each innings
    if info['toss_decision'] != 'field':
        bowling_first = toss_loser
        bowling_second = toss_winner
    else:
        bowling_first = toss_winner
        bowling_second = toss_loser

    first_innings_extras = {'bowling team': f"{bowling_first}",
                            'total': 0,
                            'wides': 0,
                            'no-balls': 0,
                            'byes': 0,
                            'leg-byes': 0,
                            'penalty': 0}
    second_innings_extras = {'bowling team': f"{bowling_second}",
                             'total': 0,
                             'wides': 0,
                             'no-balls': 0,
                             'byes': 0,
                             'leg-byes': 0,
                             'penalty': 0}
    for row in csv_f:
        if row[0] == 'info' or row[0] == 'version':
            continue
        elif row[0] != 'ball':
            break
        else:
            innings = row[1]
            over = row[2]
            team = row[3]
            batter = row[4]
            non_striker = row[5]
            bowler = row[6]
            runs = row[7]
            extras = row[8]
            wides = row[9]
            no_ball = row[10]
            byes = row[11]
            leg_bye = row[12]
            penalty = row[13]
            dismissal = row[14]
            dismissed_batter = row[15]
            # Summing how much each team scored
            if team not in team_total:
                team_total[team] = int(runs) + int(extras)
            else:
                team_total[team] += int(runs) + int(extras)
############### First innings calculations##########################
            if int(innings) == 1:
                ball_count += 1
                if batter not in first_innings_runs:
                    first_innings_runs[batter] = int(runs)
                    first_innings_scorecard[batter] = f"{runs}"
                elif batter in first_innings_runs:
                    first_innings_runs[batter] += int(runs)
                    first_innings_scorecard[batter] += f"{runs}"
                else:
                    print(f'Error in adding {batter}\'s total')
                # if not a wide, start counting deliveries
                if wides == '':
                    if batter not in first_innings_balls:
                        first_innings_balls[batter] = 1
                    else:
                        first_innings_balls[batter] += 1
                else:
                    first_innings_balls[batter] = 0
                if dismissed_batter != "":
                    first_innings_how_out[batter] = dismissal
                # Extras calculations for the first innings
                if int(extras) != 0:
                    first_innings_extras['total'] += int(float(extras))
                    if wides != '':
                        first_innings_extras['wides'] += int(float(wides))
                    elif no_ball != '':
                        first_innings_extras['no-balls'] += int(float(no_ball))
                    elif byes != '':
                        first_innings_extras['byes'] += int(float(byes))
                    elif leg_bye != '':
                        first_innings_extras['leg-byes'] += int(float(leg_bye))
                    elif penalty != '':
                        first_innings_extras['penalty'] += int(float(penalty))
###################################### BOWLERS #################################################
                # First innings bowlers
                # Calculating runs conceded for each bowler
                if bowler not in first_innings_runs_conceded:
                    first_innings_runs_conceded[bowler] = int(float(runs))
                    if wides != '' or no_ball != '' or penalty != '':
                        if wides != '':
                            first_innings_runs_conceded[bowler] += int(float(wides))
                        elif no_ball != '':
                            first_innings_runs_conceded[bowler] += int(float(no_ball))
                        else:
                            first_innings_runs_conceded[bowler] += int(float([penalty]))
                else:
                    first_innings_runs_conceded[bowler] += int(float(runs))
                    if wides != '' or no_ball != '' or penalty != '':
                        if wides != '':
                            first_innings_runs_conceded[bowler] += int(float(wides))
                        elif no_ball != '':
                            first_innings_runs_conceded[bowler] += int(float(no_ball))
                        else:
                            first_innings_runs_conceded[bowler] += int(float([penalty]))
                # Calculating overs bowled
                if bowler not in first_innings_balls_bowled and wides == '' and no_ball == '':
                    first_innings_balls_bowled[bowler] = 1
                elif wides == '' and no_ball == '':
                    first_innings_balls_bowled[bowler] += 1
                elif bowler not in first_innings_balls_bowled and not (wides == '' and no_ball == ''):
                    first_innings_balls_bowled[bowler] = 0
                for i in range(0, 5):
                    if first_innings_balls_bowled[bowler] % 6 == i:
                        first_innings_overs_bowled[bowler] = f'{int(first_innings_balls_bowled[bowler] / 6)}.{i}'
                # Maidens
                ################### STUCK TRYING TO FIGURE THIS ONE OUT ################
                if bowler not in first_innings_bowling_scorecard:
                    first_innings_bowling_scorecard[bowler] = f'{over}, {runs}, {wides}, {no_ball}, {penalty}'
                elif bowler in first_innings_bowling_scorecard:
                    first_innings_bowling_scorecard[bowler] += f'{over}, {runs}, {wides}, {no_ball}, {penalty}'
                # for k, v in first_innings_bowling_scorecard.items():
                # Wickets
                if dismissal != '' and dismissal != 'run out':
                    if bowler not in first_innings_wickets:
                        first_innings_wickets_type[bowler] = f'{dismissal}'
                        first_innings_wickets[bowler] = 1
                    else:
                        first_innings_wickets_type[bowler] += f', {dismissal}'
                        first_innings_wickets[bowler] += 1
                elif dismissal == 'run out':
                    first_innings_wickets_type['Run out'] += 1
                    first_innings_wickets['Run out'] += 1
######################### Second innings calculations#########################################
            elif int(innings) == 2:
                ball_count += 1
                if batter not in second_innings_runs:
                    second_innings_runs[batter] = int(runs)
                    second_innings_scorecard[batter] = f'{runs}'
                elif batter in second_innings_runs:
                    second_innings_runs[batter] += int(runs)
                    second_innings_scorecard[batter] += f'{runs}'
                else:
                    print("Error in adding {}'s total".format(batter))
                # if not a wide, start counting deliveries
                if wides == '':
                    if batter not in second_innings_balls:
                        second_innings_balls[batter] = 1
                    elif batter in second_innings_balls:
                        second_innings_balls[batter] += 1
                elif batter not in second_innings_balls:
                    second_innings_balls[batter] = 0
                if dismissed_batter != '':
                    second_innings_how_out[batter] = dismissal
                # Extras calculations for the second innings
                if int(extras) != 0:
                    second_innings_extras['total'] += int(float(extras))
                    if wides != '':
                        second_innings_extras['wides'] += int(float(wides))
                    elif no_ball != '':
                        second_innings_extras['no-balls'] += int(float(no_ball))
                    elif byes != '':
                        second_innings_extras['byes'] += int(float(byes))
                    elif leg_bye != '':
                        second_innings_extras['leg-byes'] += int(float(leg_bye))
                    elif penalty != '':
                        second_innings_extras['penalty'] += int(float(penalty))
                # Second innings bowlers
                # Calculating runs conceded for each bowler
                if bowler not in second_innings_runs_conceded:
                    second_innings_runs_conceded[bowler] = int(float(runs))
                    if wides != '' or no_ball != '' or penalty != '':
                        if wides != '':
                            second_innings_runs_conceded[bowler] += int(float(wides))
                        elif no_ball != '':
                            second_innings_runs_conceded[bowler] += int(float(no_ball))
                        else:
                            second_innings_runs_conceded[bowler] += int(float([penalty]))
                else:
                    second_innings_runs_conceded[bowler] += int(float(runs))
                    if wides != '' or no_ball != '' or penalty != '':
                        if wides != '':
                            second_innings_runs_conceded[bowler] += int(float(wides))
                        elif no_ball != '':
                            second_innings_runs_conceded[bowler] += int(float(no_ball))
                        else:
                            second_innings_runs_conceded[bowler] += int(float([penalty]))
                # Calculating overs bowled
                if bowler not in second_innings_balls_bowled and (wides == '' and no_ball == ''):
                    second_innings_balls_bowled[bowler] = 1
                elif wides == '' and no_ball == '':
                    second_innings_balls_bowled[bowler] += 1
                elif bowler not in second_innings_balls_bowled and not (wides == '' and no_ball == ''):
                    second_innings_balls_bowled[bowler] = 0
                for i in range(0, 5):
                    if second_innings_balls_bowled[bowler] % 6 == i:
                        second_innings_overs_bowled[
                            bowler] = f'{int(second_innings_balls_bowled[bowler] / 6)}.{i}'
                # Wickets
                if dismissal != '' and dismissal != 'run out':
                    if bowler not in second_innings_wickets:
                        second_innings_wickets_type[bowler] = f'{dismissal}'
                        second_innings_wickets[bowler] = 1
                    else:
                        second_innings_wickets_type[bowler] += f', {dismissal}'
                        second_innings_wickets[bowler] += 1
                elif dismissal == 'run out':
                    second_innings_wickets_type['Run out'] += 1
                    second_innings_wickets['Run out'] += 1
        # Assigning not outs to the batters at the end of the innings
        ####### NEED TO ADD SOMETHING FOR IF INNINGS FOR SHORTENED GAME (WEATHER)####
        if sum(first_innings_balls_bowled.values()) == 120 and dismissal == '':
            first_innings_how_out[batter] = 'Not out'
            first_innings_how_out[non_striker] = 'Not out'
        elif sum(first_innings_balls_bowled.values()) == 120 and dismissal != '':
            if batter == dismissed_batter:
                first_innings_how_out[non_striker] = 'Not out'
            else:
                first_innings_how_out[batter] = 'Not out'
        elif sum(first_innings_wickets.values()) == 10:
            if batter == dismissed_batter:
                first_innings_how_out[non_striker] = 'Not out'
            else:
                first_innings_how_out[batter] = 'Not out'
    # Assigning not outs to the batters at the end of the innings
    if team_total[bowling_second] < list(team_total.values())[1]:
        second_innings_how_out[batter] = 'Not out'
        second_innings_how_out[non_striker] = 'Not out'
    elif team_total[bowling_second] >= list(team_total.values())[1]:
        if dismissed_batter != '':
            if non_striker == dismissed_batter:
                second_innings_how_out[batter] = 'Not out'
            elif batter == dismissed_batter:
                second_innings_how_out[non_striker] = 'Not out'
        else:
            second_innings_how_out[batter] = 'Not out'
            second_innings_how_out[non_striker] = 'Not out'
    # This loop creates a breakdown of how they scored their first_innings_runs and returns
    # a dictionary with the batters name and the breakdown
    for batter_name, scores in first_innings_scorecard.items():
        listed_scores = sorted(list(scores))
        breakdown = [[score, listed_scores.count(score)] for score in set(listed_scores)]
        first_innings_runs_dict[batter_name] = sorted(breakdown)
    for batter_name, scores in second_innings_scorecard.items():
        listed_scores = sorted(list(scores))
        breakdown = [[score, listed_scores.count(score)] for score in set(listed_scores)]
        second_innings_runs_dict[batter_name] = sorted(breakdown)
    # Determining match result
    if len(list(team_total.values())) == 2:
        if team_total[bowling_second] > list(team_total.values())[1]:
            result = f'{home_team} won by {info["winner_runs"]} runs'
        elif team_total[bowling_second] == list(team_total.values())[1]:
            result = 'Tie'
        elif team_total[bowling_second] < list(team_total.values())[1]:
            result = f'{home_team} won by {info["winner_wickets"]} wickets'
    else:
        result = 'No Result'
    # Creating a batting line up for each team
    for keys, values in team_sheet.items():
        v_list = list(team_sheet.values())
        if keys == bowling_second and keys == home_team:
            first_innings_batting_list = v_list[0].split(', ')
            second_innings_batting_list = v_list[1].split(', ')
        elif keys == bowling_second and keys != home_team:
            first_innings_batting_list = v_list[1].split(', ')
            second_innings_batting_list = v_list[0].split(', ')
    # Creating innings scorecards
    for p in first_innings_batting_list:
        first_innings_batting_card[p] = {'runs': first_innings_runs.get(p),
                                         'balls_faced': first_innings_balls.get(p),
                                         'runs breakdown': first_innings_runs_dict.get(p),
                                         'how out': first_innings_how_out.get(p)}
    for p in second_innings_batting_list:
        second_innings_batting_card[p] = {'runs': second_innings_runs.get(p),
                                          'balls_faced': second_innings_balls.get(p),
                                          'runs breakdown': second_innings_runs_dict.get(p),
                                          'how out': second_innings_how_out.get(p)}
    # Prints the scorecard on a new line for each batter
    # print('First Innings:')
    # print("{" + "\n".join(
    #     "{!r}: {!r},".format(k, v) for k, v in first_innings_batting_card.items()) + "}")
    # print(f'{team_total.get(bowling_second)} - {sum(first_innings_wickets.values())}')
    # print(first_innings_extras)
    # print('Second Innings:')
    # print("{" + "\n".join(
    #     "{!r}: {!r},".format(k, v) for k, v in second_innings_batting_card.items()) + "}")
    # print(f'{team_total.get(bowling_first)} - {sum(second_innings_wickets.values())}')
    # print(second_innings_extras)
    # print(result)
    return


def build_file():
    print('hello world')


if __name__ == '__main__':
    x = read_file()
    y, z = info_grabber(x)
    (match_stats_grabber(x, y, z))
