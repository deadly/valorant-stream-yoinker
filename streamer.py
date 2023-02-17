import requests, time

class Player:
    def __init__(self, client, puuid, agentID, incognito, team):
        self.client = client
        self.puuid = puuid
        self.agentID = agentID
        self.incognito = incognito
        self.team = team
        self.name = None
        self.tag = None

        self.find_name(self.puuid)
        #self.possibleNames = self.find_possible_names()
    
    def find_name(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]

        self.name = self.filter_name(playerData['GameName'].lower())
        self.tag = playerData['TagLine'].lower()


    def filter_name(self, name):
        if ('twitch' in name):
            return name.replace('twitch', '').trim()
        if ('ttv' in name):
            return name.replace('ttv', '').trim()
        return name
    
    def find_possible_names(self):
        self.name_u = self.name.replace(' ', '_')
        self.name_d = self.name.replace(' ', '-')

        return [
            self.name,
            self.name.replace(' ', ''),
            self.name_u,
            self.name_d,
            self.name.replace(' ', '-'),
            self.name_d + self.tag,
            self.name_u + self.tag,
            f"{self.name_d}_{self.tag}",
            f"{self.name_u}_{self.tag}",
            f"{self.name_d}-{self.tag}",
            f"{self.name_u}-{self.tag}",
            f"{self.tag}_{self.name_d}",
            f"{self.tag}_{self.name_u}",
            f"{self.tag}-{self.name_d}",
            f"{self.tag}-{self.name_u}"
        ]

    def is_live(self):
        print(self.possibleNames)
        self.last = ''
        for name in self.possibleNames:
            if (name == self.last):
                continue
            self.last = name
            time.sleep(2.5)
            state = requests.get(f'https://twitch.tv/{name}').content.decode('utf-8')
            if ('isLiveBroadcast' in state):
                return name
        return False
            
        