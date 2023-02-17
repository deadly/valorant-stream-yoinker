import requests, time

class Player:
    def __init__(self, name):
        self.name = name.split('#')[0].lower()
        self.tag = name.split('#')[1].lower()
        self.filter_name()
        self.possibleNames = self.find_possible_names()
    
    def filter_name(self):
        if ('twitch' in self.name):
            self.name = self.name.replace('twitch', '').trim()
        if ('ttv' in self.name):
            self.name = self.name.replace('ttv', '').trim()
    
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
            
        