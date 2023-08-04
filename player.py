import requests, play


class Player:

    username: str
    rank: int
    list_of_plays: list[play.Play]
    playcount: int

    def __init__(self, playerid: int):
        response = requests.get(f'https://osu.ppy.sh/api/get_user?k={api_key}&u={userid}')
        player_json = response.json()[0]

        print(player_json)
        self.username = player_json["username"]
        self.rank = player_json["pp_rank"]
        p_total_score = player_json["total_score"]
        p_pp = player_json["pp_raw"]
        p_accuracy = player_json["accuracy"]
        p_playcount = player_json["playcount"]

        #return([p_username, p_rank, p_pp, p_accuracy, p_playcount, p_total_score])




