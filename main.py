from valclient.client import Client
from streamer import Player

client = Client(region="na")
client.activate()

fetched = client.coregame_fetch_player()
matchInfo = client.coregame_fetch_match(fetched['MatchID']) # data with players
puuids = []
players = []

for player in matchInfo['Players']:
    players.append(Player(
        client=client,
        puuid=player['Subject'],
        agentID=player['CharacterID'],
        incognito=player['PlayerIdentity']['Incognito'],
        team=player['TeamID']

    ))

"""playerData = client.put(endpoint="/name-service/v2/players", endpoint_type="pd", json_data=puuids)
players = []

for player in playerData:
    #print(player['CharacterID'])
    #print(player["PlayerIdentity"]["Incognito"])
    players.append(Player
    (f"{player['GameName']}#{player['TagLine']}"))

for player in players:
    if (player.is_live() != False):
        print('*******' + player.is_live())"""

for player in players:
    print("agent " + player.agentID)
    print("incognito " + str(player.incognito))
    print("team " + player.team)
