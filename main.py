from valclient.client import Client
from streamer import Player

client = Client(region="na")
client.activate()

fetched = client.coregame_fetch_player()
matchInfo = client.coregame_fetch_match(fetched['MatchID']) # data with players
puuids = []

for player in matchInfo['Players']:
    puuids.append(player['Subject'])

playerData = client.put(endpoint="/name-service/v2/players", endpoint_type="pd", json_data=puuids)
players = []

for player in playerData:
    players.append(Player(player['GameName'] + '#' + player['TagLine']))

for player in players:
    if (player.is_live() != False):
        print('*******' + player.is_live())
