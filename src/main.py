import threading
import time
from valclient.client import Client
from player import Player
from game import Game
from auto_bomb_timer import run_bomb_timer

# Paramètres intégrés (pas de settings.json)
DEFAULT_REGION = "eu"
STATE_INTERVAL = 30
TWITCH_REQ_DELAY = 3.5
SKIP_TEAM_PLAYERS = True
SKIP_PARTY_PLAYERS = True
API_RETRY_DELAY = 5  # secondes entre chaque tentative quand l'API est injoignable

running = True
seenMatches = []
logged_presence_example = False


def _is_api_unreachable(err):
    """True si l'erreur indique que l'API Valorant est injoignable."""
    err = str(err).lower()
    return (
        "unable to get headers" in err
        or "maximum recursion" in err
        or "nonetype" in err
        or "is valorant running" in err
    )


def yoinker_loop():
    """Boucle principale Stream Yoinker (match, joueurs, streamers)."""
    global seenMatches, logged_presence_example
    print("Waiting for a match to begin")
    while running:
        time.sleep(STATE_INTERVAL)
        while running:
            try:
                presence = client.fetch_presence(client.puuid)

                if not logged_presence_example:
                    print("Presence brut:", presence)
                    logged_presence_example = True

                match_presence = presence.get('matchPresenceData', {}) or {}
                party_presence = presence.get('partyPresenceData', {}) or {}

                sessionState = match_presence.get('sessionLoopState')
                if sessionState is None:
                    sessionState = party_presence.get('partyOwnerSessionLoopState')

                if sessionState is None:
                    break

                matchID = client.coregame_fetch_player()['MatchID']

                if sessionState in ("PREGAME", "INGAME") and matchID not in seenMatches:
                    print('-'*55)
                    print("Match detected")
                    seenMatches.append(matchID)
                    matchInfo = client.coregame_fetch_match(matchID)
                    players = []

                    for player in matchInfo['Players']:
                        if (client.puuid == player['Subject']):
                            localPlayer = Player(
                                client=client,
                                puuid=player['Subject'].lower(),
                                agentID=player['CharacterID'].lower(),
                                incognito=player['PlayerIdentity']['Incognito'],
                                team=player['TeamID']
                            )
                        else:
                            players.append(Player(
                                client=client,
                                puuid=player['Subject'].lower(),
                                agentID=player['CharacterID'].lower(),
                                incognito=player['PlayerIdentity']['Incognito'],
                                team=player['TeamID']
                            ))

                    print("\nPlayers in match:")
                    for p in [localPlayer] + players:
                        print(f"{p.full_name} - {p.team} {p.agent}")

                    try:
                        party = client.fetch_party()
                    except (RecursionError, Exception) as api_err:
                        if not _is_api_unreachable(api_err) and "core" not in str(api_err).lower():
                            raise
                        party = None
                        print("(API party indisponible, recherche Twitch sans filtre party)")

                    currentGame = Game(party=party, matchID=matchID, players=players, localPlayer=localPlayer)
                    print("\nFinding hidden names\n")
                    currentGame.find_hidden_names(players)

                    print("\nFinding potential streamers\n")
                    currentGame.find_streamers(players, TWITCH_REQ_DELAY, SKIP_TEAM_PLAYERS, SKIP_PARTY_PLAYERS)
                break

            except RecursionError:
                print("API injoignable, nouvel essai dans", API_RETRY_DELAY, "s...")
                time.sleep(API_RETRY_DELAY)
            except Exception as e:
                if _is_api_unreachable(e):
                    print("API injoignable, nouvel essai dans", API_RETRY_DELAY, "s...")
                    time.sleep(API_RETRY_DELAY)
                else:
                    err = str(e)
                    if "core" not in err:
                        print("An error occurred:", e)
                    break


if __name__ == "__main__":
    print('Valorant Stream Yoinker + Bomb Timer')
    print('https://github.com/Sweizeur/valorant-stream-yoinker-bomb-timer')
    print('Based on https://github.com/deadly/valorant-stream-yoinker')

    client = Client(region=DEFAULT_REGION)
    client.activate()

    thread = threading.Thread(target=yoinker_loop, daemon=True)
    thread.start()

    run_bomb_timer()
