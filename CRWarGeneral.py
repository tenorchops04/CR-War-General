import requests
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Prompt user for clan tag. raw_input ensures that inout is of type string so that we can append it to other strings.
clanTag = raw_input("Enter clan tag: ")
print('')

# Used to build the API request.
base = 'https://api.royaleapi.com/'
clanInfo = 'clan/' + clanTag
warLog = 'clan/' + clanTag + '/warlog'

# Requests clan information.
urlClan = base + clanInfo

# Requests war log information of clan.
urlWarLog = base + warLog

headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzM2MSwiaWRlbiI6IjUzMDY5MzE0MzYxMjM1ODY2NiIsIm1kIjp7InVzZXJuY"
            "W1lIjoiVGVub3JjaG9wcyIsImRpc2NyaW1pbmF0b3IiOiIwNDU5Iiwia2V5VmVyc2lvbiI6M30sInRzIjoxNTc2NDg4ODE2NTQ0fQ.1FlI"
            "7ZZUSOjs0mg9QVAwEsIbxXQQdiAxTJT-0iGW4xg"
    }

# Get the JSON data from the API.
responseClan = requests.request("GET", urlClan, headers=headers)
responseWL = requests.request("GET",urlWarLog, headers = headers)
clanData = responseClan.json()
warLogData = responseWL.json()

# Creates an object Player with a name and player tag.
class Player:

    def __init__(self, name, tag, level, warDayWins):
        self.name = name
        self.tag = tag
        self.level = level
        self.warDayWins = warDayWins
        self.warsIn = 0
        self.battleCount = 0
        self.warWins = 0
        self.warLosses = 0
        self.missedBattles = 0
        self.winRatio = 0

    def __repr__(self):
        return "Player: %s\n" \
               "Tag: %s\n" \
               "Level: %s\n" \
               "Total War Wins: %s\n" \
               "Wars Participated:%s\n" \
               "War Battles: %s\n" \
               "War Wins: %s\n" \
               "War Losses: %s\n" \
               "Battles Missed: %s" \
               % (self.name, self.tag, self.level, self.warDayWins, self.warsIn, self.battleCount, self.warWins,
                  self.warLosses, self.missedBattles)

    def __str__(self):
        return "Player: %s | " \
               "Tag: %s | " \
               "Level: %s |" \
               "Total War Wins: %s | " \
               "Wars Participated:%s | " \
               "War Battles: %s | " \
               "War Wins: %s | " \
               "War Losses: %s | " \
               "Battles Missed: %s | " \
               "Win Ratio: %.2f " \
               % (self.name, self.tag, self.level, self.warDayWins, self.warsIn, self.battleCount, self.warWins,
                  self.warLosses, self.missedBattles, self.winRatio)

    def incWarsIn(self):
        self.warsIn += 1;

    def incBattleCount(self, n):
        self.battleCount += n

    def incWarWins(self, n):
        self.warWins += n

    def incrWarLosses(self, n):
        self.warLosses += n

    def incMissedBattles(self, n):
        self.missedBattles += n

    def calcWinRatio(self):
        if self.battleCount == 0:
            self.winRatio = 0

        else:
            self.winRatio = self.warWins / float(self.battleCount) * 100

# Create a list of Player objects which will have each member of the clan.
playerList = []
playerDic = {}

# Create individual players and add them to a list playerList.
for p in clanData['members']:
    playerName = p['name']
    playerTag = p['tag']

    # Get JSON data for every individual player in the clan using that player's tag.
    playerEndPoint = 'player/' + playerTag
    urlPlayer = base + playerEndPoint
    responsePlayer = requests.request("GET", urlPlayer, headers=headers)
    playerData = responsePlayer.json()

    playerLevel = playerData['stats']['level']
    playerWarWins = playerData['games']['warDayWins']

    playerList.append(Player(playerName, playerTag, playerLevel, playerWarWins))

# Populate a Dictionary of Players with their tag as a key and the Player object as a value.
for player in playerList:
    playerDic[player.tag] = player

# Fill object Players with information from playerList.
for war in warLogData:
    for p in war['participants']:
        player = playerDic.get(p['tag'])
        if player != None:
            player.incWarsIn()
            player.incBattleCount(p['battleCount'])
            player.incWarWins(p['wins'])
            player.incrWarLosses(p['battleCount'] - p['wins'] - p['battlesMissed'])
            player.incMissedBattles(p['battlesMissed'])
            player.calcWinRatio()

# Print each players information.
# for tag in playerDic:
#     player = playerDic[tag]
#     print player

# Sort players in playerList by highest win ratio.
playerList.sort(key = lambda x: x.winRatio, reverse= True)

for player in playerList:
    print player