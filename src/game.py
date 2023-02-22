class Game:
    def __init__(self, matchID, players, localPlayer):
        self.matchID = matchID
        self.players = players
        self.localPlayer = localPlayer
        self.teamPlayers = self.find_team_players(self.localPlayer, self.players)
    
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

    def find_streamers(self, players, twitchReqDelay, skipTeamPlayers):
        self.streamers = []
        for player in self._progressBar(players,prefix='Progress:',suffix='Complete',length=len(players)):
            if (skipTeamPlayers and player in self.teamPlayers):
                continue
            
            if (player.is_live(twitchReqDelay)):
                self.streamers.append(f"twitch.tv/{player.name}")
            
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