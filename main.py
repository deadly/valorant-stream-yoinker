from valclient.client import Client
from streamer import Player

client = Client(region="na")
client.activate()

fetched = client.coregame_fetch_player()
matchInfo = client.coregame_fetch_match(fetched['MatchID'])
players = []

for player in matchInfo['Players']:
    players.append(Player(
        client=client,
        puuid=player['Subject'],
        agentID=player['CharacterID'],
        incognito=player['PlayerIdentity']['Incognito'],
        team=player['TeamID']
    ))

for player in players:
    print(f"{player.name}#{player.tag} ({player.agent}): streamer mode: {player.incognito} team: {player.team}")
    #print("agent " + player.agentID)
    #print("name " + player.name)
    #print("tag " + player.tag)
    #print("incognito " + str(player.incognito))
    #print("team " + player.team)
    print(player.is_live())
