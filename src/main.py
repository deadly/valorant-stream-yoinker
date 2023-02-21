import json, time
from valclient.client import Client
from player import Player
from game import Game

running = True
seenMatches = []

print('Valorant Stream Yoinker by https://github.com/deadly')

with open('settings.json', 'r') as f:
    data = json.load(f)
    ranBefore = data['ran']
    region = data['region']
    stateInterval = data['stateInterval']
    twitchReqDelay = data['twitchReqDelay']

if (ranBefore == False):
    region = input("Enter your region: ").lower()
    client = Client(region=region)
    client.activate()

    with open('settings.json', 'w') as f:
            data['ran'] = True
            data['region'] = region
            json.dump(data, f)
else:
    client = Client(region=region)
    client.activate()

print("Waiting for a match to begin")
while (running):
    time.sleep(stateInterval)
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        matchID = client.coregame_fetch_player()['MatchID']

        if (sessionState == "INGAME" and matchID not in seenMatches):
            print('-'*10)
            print("Match detected")
            seenMatches.append(matchID)
            matchInfo = client.coregame_fetch_match(matchID)
            players = []

            for player in matchInfo['Players']:
                players.append(Player(
                    client=client,
                    puuid=player['Subject'],
                    agentID=player['CharacterID'],
                    incognito=player['PlayerIdentity']['Incognito'],
                    team=player['TeamID']
                ))
            
            currentGame = Game(matchID=matchID, players=players)

            found = False
            print("\nFinding hidden names\n")
            currentGame.find_hidden_names(players)
            
            print("\nFinding potential streamers\n")
            currentGame.find_streamers(players, twitchReqDelay)

    except Exception as e:
        if ("core" not in str(e)):
            print("An error occurred:", e)
