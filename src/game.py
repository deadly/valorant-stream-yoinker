import webbrowser

try:
    from win10toast_click import ToastNotifier
    _toaster = ToastNotifier()
except ImportError:
    _toaster = None


class Game:
    def __init__(self, party, matchID, players, localPlayer):
        self.matchID = matchID
        self.players = players
        self.localPlayer = localPlayer
        self.teamPlayers = self.find_team_players(self.localPlayer, self.players)
        self.partyPlayers = self.find_party_members(party)
    
    def find_hidden_names(self, players):
        self.found = False
        for player in players:
            if (player.incognito):
                self.found = True
                print(f"{player.full_name} - {player.team} {player.agent}")
        if not self.found:
            print("No hidden names found")
    
    # progressBar credit: https://stackoverflow.com/users/2206251/
    @staticmethod
    def _progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        total = len(iterable)
        if total == 0:
            # Rien à afficher, éviter une division par zéro
            print(f'{prefix} |{"-" * length}| 0.0% {suffix}')
            return
        # Progress Bar Printing Function
        def printProgressBar(iteration):
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

    @staticmethod
    def _notify_streamer(player, url):
        """Affiche une notification Windows pour un streamer trouvé, ouvre le lien au clic."""
        if _toaster is None:
            # Fallback si win10toast_click n'est pas installé
            print(f"[NOTIF] {player.full_name} est en live: {url}")
            return

        def open_stream():
            webbrowser.open(url)

        _toaster.show_toast(
            "Valorant Stream Yoinker + Bomb Timer",
            f"{player.full_name} est en live sur Twitch",
            duration=10,
            threaded=True,
            callback_on_click=open_stream,
        )

    def find_streamers(self, players, twitchReqDelay, skipTeamPlayers, skipPartyPlayers):
        self.streamers = []

        for player in self._progressBar(players,prefix='Progress:',suffix='Complete',length=len(players)):
            if (skipTeamPlayers) and (player in self.teamPlayers):
                continue

            if (skipPartyPlayers) and (player.puuid in self.partyPlayers):
                continue
            
            live_name = player.is_live(twitchReqDelay)
            if live_name:
                url = f"https://twitch.tv/{live_name}"
                self.streamers.append(url)
                self._notify_streamer(player, url)
            
        if len(self.streamers) > 0:
            for streamer in self.streamers:
                print(f"Live: {streamer}")
        else:
            print("No streamers found")
    
    def find_team_players(self, localPlayer, players):
        team_players = []
        
        for player in players:
            if (player.team == localPlayer.team):
                team_players.append(player)
        
        return team_players
    
    def find_party_members(self, party):
        members = []
        if party is None or not isinstance(party, dict):
            return members
        for member in party.get('Members') or []:
            members.append(member['Subject'].lower())
        return members