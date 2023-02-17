import json, time
from valclient.client import Client
from streamer import Player

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

# progressBar credit: https://stackoverflow.com/users/2206251/
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

print("Waiting for a match to begin")
while (running):
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
            
            found = False
            print("\nFinding hidden names\n")
            for player in players:
                if (player.incognito):
                    found = True
                    print(f"{player.full_name} - {player.team} {player.agent}")
            
            if not found:
                print("No hidden names found")
            
            streamers = []
            print("\nFinding potential streamers\n")
            for player in progressBar(players, prefix='Progress:',suffix='Complete',length=len(players)):
                if (player.is_live(twitchReqDelay)):
                    streamers.append(f"twitch.tv/{player.name}")
            
            if len(streamers) > 0:
                for streamer in streamers:
                    print(f"Live: {streamer}")
            else:
                print("No streamers found")

    except Exception as e:
        if ("core" not in str(e)):
            print(e)
    time.sleep(stateInterval)
