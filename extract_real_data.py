import urllib.request
import ssl
import json

#---------------- Settings ----------------

t2_towers_ID=[ "Turret_T2_L_03_A",
                "Turret_T2_C_05_A",
                "Turret_T2_R_03_A",
                "Turret_T2_L_02_A",
                "Turret_T2_C_04_A",
                "Turret_T2_R_02_A",
                "Turret_T2_L_01_A",
                "Turret_T2_C_03_A",
                "Turret_T2_R_01_A",
                "Turret_T2_C_02_A",
                "Turret_T2_C_01_A"]

t1_towers_ID=["Turret_T1_L_03_A",
                "Turret_T1_C_05_A",
                "Turret_T1_R_03_A",
                "Turret_T1_L_02_A",
                "Turret_T1_C_04_A",
                "Turret_T1_R_02_A",
                "Turret_T1_L_01_A",
                "Turret_T1_C_03_A",
                "Turret_T1_R_01_A",
                "Turret_T1_C_02_A",
                "Turret_T1_C_01_A"]

t2_inhibs = ["Barracks_T2_L1", "Barracks_T2_C1", "Barracks_T2_R1"]

#---------------- Methods ----------------

def fetch_game_data():
    api_url = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(api_url, context=context) as response:
            data = response.read()
            return json.loads(data.decode())
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None

    
def get_level_difference(data):
    t1_level_sum = sum(player["level"] for player in data["allPlayers"][:5])
    t2_level_sum = sum(player["level"] for player in data["allPlayers"][5:10])
    avg_level_t1 = t1_level_sum / 5
    avg_level_t2 = t2_level_sum / 5
    return avg_level_t1 - avg_level_t2

    
def get_teams(x):
    t1_players = []
    t2_players = []
    for i in range(0,5):
        t1_players.append(x["allPlayers"][i]["summonerName"])
        t2_players.append(x["allPlayers"][i+5]["summonerName"])
    return t1_players,t2_players

#what team is active player in?
def team_of_active_player(x):
    name_of_active_player = x['activePlayer']["summonerName"]
    t1_players, _ = get_teams(x)
    if name_of_active_player in t1_players:
        return "t1"
    else:
        return "t2"
    
# def get_tower_kills(data):
#     tower_kills = {"t1": 0, "t2": 0}
#     for event in data["events"]['Events']:
#         if event["EventName"] == "TurretKilled":
#             tower_id = event['TurretKilled']
#             if tower_id in t1_towers_ID:
#                 tower_kills["t1"] += 1
#             elif tower_id in t2_towers_ID:
#                 tower_kills["t2"] += 1
#     active_team = "t1" if team_of_active_player(data) == "t1" else "t2"
#     return tower_kills[active_team]

    
def get_assist_difference(x):
    t1_assists = sum(player["scores"]["assists"] for player in x["allPlayers"][:5])
    t2_assists = sum(player["scores"]["assists"] for player in x["allPlayers"][5:10])
    assist_difference = t1_assists - t2_assists
    return assist_difference if team_of_active_player(x) == "t1" else -assist_difference
    
    
def get_death_difference(x):
    t1_deaths = sum(player["scores"]["deaths"] for player in x["allPlayers"][:5])
    t2_deaths = sum(player["scores"]["deaths"] for player in x["allPlayers"][5:10])
    death_diff = t1_deaths - t2_deaths
    return death_diff if team_of_active_player(x) == "t1" else -death_diff

    
def get_kill_difference(x):
    kills_t1 = sum(player["scores"]["kills"] for player in x["allPlayers"][:5])
    kills_t2 = sum(player["scores"]["kills"] for player in x["allPlayers"][5:10])
    kill_diff = kills_t1 - kills_t2
    return kill_diff if team_of_active_player(x) == "t1" else -kill_diff

    
def get_dragons(x):
    t1_dragons = 0
    t2_dragons = 0
    t1_players, _ = get_teams(x)
    for event in x["events"]['Events']:
        if event["EventName"] == "DragonKill":
            if event['KillerName'] in t1_players:
                t1_dragons += 1
            else:
                t2_dragons += 1
    return t1_dragons if team_of_active_player(x) == "t1" else t2_dragons

    
    
def get_first_dragon(x):
    team_view = team_of_active_player(x)
    t1_players, _ = get_teams(x)
    for event in x["events"]['Events']:
        if event["EventName"] == "DragonKill":
            dragon_killer_team = "t1" if event['KillerName'] in t1_players else "t2"
            return 1 if dragon_killer_team == team_view else 0
    return 0

    
def get_first_tower(x):
    for event in x["events"]['Events']:
        if event["EventName"] == "TurretKilled":
            tower_taker = "t1" if event["TurretKilled"] in t1_towers_ID else "t2"
            return 1 if tower_taker == team_of_active_player(x) else 0
    return 0


def first_blood(x):
    t1_players, _ = get_teams(x)
    fb_recipient =""
    
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "FirstBlood":
            if x["events"]['Events'][i]["Recipient"] in t1_players:
                fb_recipient = "t1"
            else:
                fb_recipient = "t2"
    
    if team_of_active_player(x) == "t1" and fb_recipient == "t1":
        return 1
    elif team_of_active_player(x) == "t2" and fb_recipient == "t2":
        return 1
    else:
        return 0
    
def get_inhibitors(x):
    t1_inhibs_destroyed = 0
    t2_inhibs_destroyed = 0
    for event in x["events"]['Events']:
        if event['EventName'] == 'InhibKilled':
            if event['InhibKilled'] in t2_inhibs:
                t1_inhibs_destroyed += 1
            else:
                t2_inhibs_destroyed += 1
    return t1_inhibs_destroyed if team_of_active_player(x) == "t1" else t2_inhibs_destroyed

    
def get_towers(x):
    t1_tower_count, t2_tower_count = 0, 0
    for event in x["events"]['Events']:
        if event['EventName'] == 'TurretKilled':
            if event["TurretKilled"] in t1_towers_ID:
                t2_tower_count += 1
            elif event["TurretKilled"] in t2_towers_ID:
                t1_tower_count += 1
    return t1_tower_count if team_of_active_player(x) == "t1" else t2_tower_count

    
def get_heralds(x):
    t1_herald_kills, t2_herald_kills = 0, 0
    t1_players, _ = get_teams(x)

    for event in x["events"]['Events']:
        if event["EventName"] == "HeraldKill":
            if event["KillerName"] in t1_players:
                t1_herald_kills += 1
            else:
                t2_herald_kills += 1
    return t1_herald_kills if team_of_active_player(x) == "t1" else t2_herald_kills

    
def get_first_inhibitor(x):
    for event in x["events"]['Events']:
        if event["EventName"] == "InhibKilled":
            inhib_taker = "t2" if event["InhibKilled"] in t2_inhibs else "t2"
            return 1 if inhib_taker == team_of_active_player(x) else 0
    return 0
    
def get_cs_difference(x):
    t1_cs, t2_cs = 0, 0
    for i in range(5):
        t1_cs += x["allPlayers"][i]['scores']["creepScore"]
        t2_cs += x["allPlayers"][i + 5]['scores']["creepScore"]
    cs_difference = t1_cs - t2_cs
    return cs_difference if team_of_active_player(x) == "t1" else -cs_difference
    
def get_jungle_cs_difference(x):
    t1_jungle_cs, t2_jungle_cs = 0, 0
    for player in x["allPlayers"]:
        if player['position'] == "JUNGLE":
            if player["team"] == "ORDER":  # ORDER is considered as team1
                t1_jungle_cs += player['scores']["creepScore"]
            else:
                t2_jungle_cs += player['scores']["creepScore"]
    jungle_cs_gap = t1_jungle_cs - t2_jungle_cs
    return jungle_cs_gap if team_of_active_player(x) == "t1" else -jungle_cs_gap
    
def timestamp(x):
    return x['gameData']["gameTime"]

def current_stats(x):
    current_game_stats = {}
    current_game_stats["time"] = timestamp(x)
    current_game_stats["firstBlood"] = first_blood(x)
    current_game_stats["firstTower"] = get_first_tower(x)
    current_game_stats["firstInhibitor"] = get_first_inhibitor(x)
    current_game_stats["firstDragon"] = get_first_dragon(x)
    # current_game_stats["firstBaron"] = first_baron(x)
    current_game_stats["tower_amount"] = get_towers(x)
    current_game_stats["inhibs_amount"] = get_inhibitors(x)
    # current_game_stats["firstRiftHerald"] = first_herald(x)
    # current_game_stats["baron_amount"] = get_baron_amount(x)
    current_game_stats["Dragons_Amount"] = get_dragons(x)
    current_game_stats["riftHeralds_amount"] = get_heralds(x)
    current_game_stats["Kills_Diff"] = get_kill_difference(x)
    current_game_stats["Death_Diff"] = get_death_difference(x)
    current_game_stats["Assist_Diff"] = get_assist_difference(x)
    current_game_stats["Lv_Diff"] = get_level_difference(x)
    current_game_stats["cs_Diff"] = get_cs_difference(x)
    current_game_stats["jg_cs_Diff"] = get_jungle_cs_difference(x)
    current_game_stats["win_probability"] = 0.5
    return current_game_stats