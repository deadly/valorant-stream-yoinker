import requests, time, random

proxy_list = []
x = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&simplified=true', stream=True)
for y in x.iter_lines():
    if y: 
        proxy_list.append({'http': f"socks4://{y.decode().strip()}"})
        


agentMap = {
    "add6443a-41bd-e414-f6ad-e58d267f4e95": "Jett",
    "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc": "Reyna",
    "f94c3b30-42be-e959-889c-5aa313dba261": "Raze",
    "7f94d92c-4234-0a36-9646-3a87eb8b5c89": "Yoru",
    "eb93336a-449b-9c1b-0a54-a891f7921d69": "Phoenix",
    "bb2a4828-46eb-8cd1-e765-15848195d751": "Neon",
    "5f8d3a7f-467b-97f3-062c-13acf203c006": "Breach",
    "6f2a04ca-43e0-be17-7f36-b3908627744d": "Skye",
    "320b2a48-4d9b-a075-30f1-1f93a9b638fa": "Sova",
    "601dbbe7-43ce-be57-2a40-4abd24953621": "Kayo",
    "1e58de9c-4950-5125-93e9-a0aee9f98746": "Killjoy",
    "117ed9e3-49f3-6512-3ccf-0cada7e3823b": "Cypher",
    "569fdd95-4d10-43ab-ca70-79becc718b46": "Sage",
    "22697a3d-45bf-8dd7-4fec-84a9e28c69d7": "Chamber",
    "8e253930-4c05-31dd-1b6c-968525494517": "Omen",
    "9f0d8ba9-4140-b941-57d3-a7ad57c6b417": "Brimstone",
    "41fb69c1-4189-7b37-f117-bcaf1e96f1bf": "Astra",
    "707eab51-4836-f488-046a-cda6bf494859": "Viper",
    "dade69b4-4f5a-8528-247b-219e5a1facd6": "Fade",
    "95b78ed7-4637-86d9-7e41-71ba8c293152": "Harbor",
    "e370fa57-4757-3604-3648-499e1f642d3f": "Gekko",
    "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235": "Deadlock"
}

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
            
        
