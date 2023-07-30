#%%
import time
import requests
import bisect

apiKey = "ee4b4818-0966-4495-b6de-958ea38bf82c"
allPossibleStats = ['prestigeTimes', '_id', '__v', 'assists', 'blocksBroken', 'chatMessages', 'contracts', 'damageDealt',
 'damageRatio', 'damageReceived', 'darkPants', 'deaths', 'fishedAnything', 'gapples', 'gheads', 'gold', 'highestStreak', 
 'kdr', 'kills', 'kingsQuests', 'lavaBuckets', 'leftClicks', 'lifetimeGold', 'lifetimeRenown', 'nightQuests', 'playtime', 
 'renown', 'sewerTreasures', 'soups', 'tierThrees', 'wheatFarmed', 'xp', 'blocksPlaced', 'arrowHits', 'arrowShots',
 'enderchestOpened', 'joins', 'jumpsIntoPit', 'launcherLaunches', 'totalJumps', 'bounty', 'bowAccuracy', 'bowDamageDealt',
 'bowDamageReceived', 'contractsRatio', 'contractsStarted', 'darkPantsT2', 'diamondItemsPurchased', 'fishedFish', 
 'fishingRodCasts', 'genesisPoints', 'goldHourly', 'hiddenJewelsTriggered', 'kadr', 'killAssistHourly', 'killsHourly', 
 'meleeDamageDealt', 'meleeDamageReceived', 'swordHits', 'tierOnes', 'tierTwos', 'xpHourly', 'bowDamageRatio', 
 'meleeDamageRatio', 'searches', 'bountiesClaimed', 'ingotsGold', 'ingotsPickedUp', 'ragePotatoesEaten', 'vampireHealedHp', 
 'obsidianBroken']      


def makeAPIcall(url):
    request = requests.get(url)
    request.content
    request.text
    return request.json()

def getGuild():
    infos = makeAPIcall('https://api.hypixel.net/guild?key=' + apiKey + '&name=noodle%20club')
    guild = infos["guild"]
    members = guild["members"]
    list = []
    for i in members:
        list.append(i["uuid"])
    return list

def getGroupPitStat(list, stat):
    ordered = []
    counter = 0
    for i in list:
        counter += 1
        infos = makeAPIcall('https://pitpanda.rocks/api/playerdoc/' + i)
        if (not infos["success"] and infos["error"] == "Player has not played the Pit") or stat not in infos["Doc"]:
            saidStat = 0
            ign = i
        else:
            doc = infos["Doc"]
            if stat == "prestigeTimes":
                saidStat = len(doc[stat])
            else:
                saidStat = doc[stat]     
            ign = doc["name"]   
        player = [saidStat, ign]
        bisect.insort(ordered, player)
        
    return ordered[::-1]

def getPitPlayers():
    topplayers = []
    for i in range(731, 2000):        # I-60
        
        infos = makeAPIcall('https://pitpanda.rocks/api/leaderboard/xp?page=' + str(i))
        lb = infos["leaderboard"]
        
        for i in lb:    
            topplayers.append(i["uuid"])
            print(i["name"])
            
    file = open('players.txt', "a")
    for j in topplayers:
        file.write(j + '\n')
    file.close()
        
def gatherPitPerkUses():
    file = open('players.txt', "r")
    perksList = [3, 4, 145, 170, 188, 258, 260, 261, 264, 266, 280, 282, 287, 296, 297, 301, 302, 316, 327, 331, 346, 352, 363, 366, 373, 376, 381, 383, 397]
    perkCount = [0 for i in range(29)]
    counter = 0
    
    for player in file:
        infos = makeAPIcall('https://pitpanda.rocks/api/players/' + player + '?apikey=2b7fdf7e-6154-4212-8e9d-9bac9eb4e40b')
        if not infos["success"]:
            print('Zzzz')
            time.sleep(61)
            makeAPIcall('https://pitpanda.rocks/api/players/' + player + '?apikey=2b7fdf7e-6154-4212-8e9d-9bac9eb4e40b')
        if not "data" in infos:
            continue
        data = infos["data"]
        inventories = data["inventories"]
        perks = inventories["perks"]
        print(data["name"])
        counter += 1
        
        for p in perks:
            if p:
                used = perksList.index(int(p["id"]))
                perkCount[used] += 1   
                       
    file.close()
    return perkCount
        

#%%