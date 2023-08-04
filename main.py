import time

from info import *
import requests
from sheets import *



def get_username(playerid: int) -> str:
    print(f'https://osu.ppy.sh/api/get_user?k={api_key}&u={userid}')
    response = requests.get(f'https://osu.ppy.sh/api/get_user?k={api_key}&u={userid}')
    if response.json():
        player_json = response.json()[0]
        return player_json['username']
    else: return "None"

def get_team_name(playerid: int) -> str:
    return playerid_to_team[playerid]

def get_mod_combo(modbit: int) -> list:
    enabledMods: list = []
    modBits: list = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256,
                     512, 1024, 2048, 4096, 8192, 16384]
    mods: list = ["None", "NoFail", "Easy", "TouchDevice", "Hidden", "HardRock",
                  "SuddenDeath", "DoubleTime", "Relax", "HalfTime", "Nightcore",
                  "Flashlight"]

    while modbit > 0:
        i = 0
        while i < len(modBits):
            if modBits[i] > modbit:
                enabledMods.append(mods[i - 1])
                modbit = modbit - modBits[i-1]
                break
            i += 1

    return enabledMods

def calculate_accuracy(a: int, b: int, c: int, miss: int):
    numerator = ((300 * a) + (100 * b) + (50 * c))
    denominator = (300 * (a+b+c+miss))

    return float(numerator) / denominator

def modlist_to_str(modlist: list) -> str:
    output: str = ''
    for mods in modlist:
        output += str(mods)




i = 2
for match_id in list_of_matches:
    response = requests.get(f'https://osu.ppy.sh/api/get_match?k={api_key}&mp={match_id}')
    mp_json = response.json()

    match = mp_json['match']
    games = mp_json['games']

    # get match information (APPEND THESE LATER)
    match_name = match['name']
    match_id = match['match_id']


    # go through games and find individual score
    for game in games:

        # get map information
        map_id: int = int(game['beatmap_id'])

        response = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={api_key}&b={map_id}')
        beatmaps = response.json()
        beatmap = beatmaps[0]

        map_name: str = beatmap['title']
        diff_name = beatmap['version']
        star_rating: float = float(beatmap['difficultyrating'])
        max_combo: int = beatmap['max_combo']

        aim: int = beatmap['diff_aim']
        speed: int = beatmap['diff_speed']


        mod_list: list = get_mod_combo(int(game['mods']))
        mod_used: str = modlist_to_str(mod_list)
        scores = game['scores']

        for score in scores:
            userid = int(score["user_id"])
            player_name = get_username(userid)
            team_name = get_team_name(userid)

            score_achieved: int = int(score['score'])

            count300s = int(score['count300'])
            count100s = int(score['count100'])
            count50s = int(score['count50'])
            countmiss = int(score['countmiss'])

            accuracy: float = calculate_accuracy(count300s,count100s,
                                                 count50s,countmiss)

            max_combo_achieved = int(score['maxcombo'])

            # get player information

            response = requests.get(f'https://osu.ppy.sh/api/get_user?k={api_key}&u={userid}')
            player_rank: int = 0
            player_pp: int = 0
            player_name: str = "N/A"
            player_playcount: int = 0

            if response.json():
                users = response.json()
                user = users[0]

                player_rank: int = user['pp_rank']
                player_pp: int = user['pp_raw']
                player_name: int = user['username']
                player_playcount: int = user['playcount']

            score2: list = [match_name, match_id, userid, player_name,
                            team_name, map_id, map_name, mod_used, star_rating,
                            score_achieved, accuracy, max_combo_achieved,
                            max_combo, player_rank, player_pp, player_playcount,
                            aim, speed, count300s, count100s, count50s,
                            countmiss]
            print(score2)

            range = "Raw Data!A" + str(i)
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range=range,
                                            valueInputOption="USER_ENTERED",
                                            body={"values": [score2]}).execute()
            i+=1
            time.sleep(1)

