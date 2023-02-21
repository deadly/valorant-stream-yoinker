class Game:
    def init(self, client, matchID, players):
        self.matchID = matchID
        self.players = players
    
    def find_hidden_names(self, players):
        found = False
        for player in players:
            if (player.incognito):
                found = True
                print(f"{player.full_name} - {player.team} {player.agent}")
        if not found:
            print("No hidden names found")
    
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

    def find_streamers(self, players):
        
