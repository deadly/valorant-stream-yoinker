import requests, time, random

proxy_list = []
x = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&simplified=true', stream=True)
for y in x.iter_lines():
    if y: 
        proxy_list.append({'http': f"socks4://{y.decode().strip()}"})
        
agentMap = {}

try:
    reqAgents = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true")
    reqAgents = reqAgents.json()
    Agents = reqAgents['data']
    for agent in Agents:
        agentMap[agent['uuid']] = agent['displayName']
    print("Finished Updating Agents")
except Exception as e:
    print(e)
        
class Player:
    def __init__(self, client, puuid, agentID, incognito, team):
        self.client = client
        self.puuid = puuid
        self.agent = agentMap[agentID]
        self.incognito = incognito
        self.team = self.side(team)
        self.name = self.filter_name(self.set_name(puuid).split('#')[0])
        self.full_name = self.set_name(puuid)
        self.tag = self.set_name(puuid).split('#')[1]
        self.possibleNames = self.find_possible_names()

    def side(self, color):
        if (color == "Blue"):
            return "Defending"
        else:
            return "Attacking"
    
    def set_name(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]

        return f"{playerData['GameName']}#{playerData['TagLine']}"

    def filter_name(self, name):
        if ('twitch' in name):
            return name.replace('twitch', '').strip()
        if ('ttv' in name):
            return name.replace('ttv', '').strip()
        return name
    
    def find_possible_names(self):
        self.name_u = self.name.replace(' ', '_')
        self.name = self.name.replace(' ', '')

        return list(set([
            self.name,
            self.name + self.tag,
            self.name_u,
            self.name_u + self.tag,
            self.tag + self.name,
            self.tag + self.name_u,
            f"{self.name}_{self.tag}",
            f"{self.tag}_{self.name}",
            f"{self.name_u}_{self.tag}",
            f"{self.tag}_{self.name_u}",
        ]))

    def is_live(self, delay):
        for name in self.possibleNames:
            time.sleep(delay)
            state = requests.get(f'https://twitch.tv/{name}', proxies=random.choice(proxy_list)).content.decode('utf-8')
            if ('isLiveBroadcast' in state):
                return name
        return False
            
        
