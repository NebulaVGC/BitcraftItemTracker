import requests
import re
import json
from multiprocessing import Pool
async def checkPlayers(itemIDs):
    raw = requests.get('https://bitjita.com/claims/648518346353424439').text
    start = raw.find("members:")
    fin = raw[start:].find("}]")
    playerRaw = raw[start + 8:start + fin + 2]
    playerRaw = playerRaw.strip()
    playerRaw = playerRaw.rstrip(',')
    playerRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', playerRaw)
    playerRaw = playerRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')

    playerJSON = json.loads(playerRaw)

    #Tracked Items -> players with tracked items in inventory + amount [userID, amount]

    itemToPlayer = {}
    s = requests.Session()
    playerList = []
    
    for player in playerJSON:
        playerList.append([player['playerEntityId'], itemIDs])
    with Pool(200) as p:
        x = p.starmap(getPlayersWithItem, playerList)
    return x

def getPlayersWithItem(player, itemIDs):
    raw = requests.get(f'https://bitjita.com/players/{player}#inventory').text
    start = raw.find("player:") 
    fin = raw[start:].find("items:")
    playerRaw = raw[start + 7: start + fin]
    start = playerRaw.find("inventories:")
    inventoryRaw = playerRaw[start + 12:]
    playerRaw = playerRaw[:start]
    playerRaw = playerRaw.strip()
    playerRaw = playerRaw.rstrip(',')
    playerRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', playerRaw)
    playerRaw = playerRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')
    playerRaw = re.sub(r'(?<!\d)\.(\d)', r'0.\1', playerRaw)

    
    inventoryRaw = inventoryRaw.strip()
    inventoryRaw = inventoryRaw.rstrip(',')
    inventoryRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', inventoryRaw)
    inventoryRaw = inventoryRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')
    inventoryRaw = re.sub(r'(?<!\d)\.(\d)', r'0.\1', inventoryRaw)
    inventoryRaw = inventoryRaw + "}"
    try:
        playerJSON = json.loads(playerRaw)
        inventoryJSON = json.loads(inventoryRaw)
    except Exception as e:        
        return
    pockets = inventoryJSON['inventories']
    nameAndItems = []
    for pocket in pockets:
        if(pocket['inventoryName'] == "Inventory"):
                for item in pocket['pockets']:
                    if(str(item['contents']['itemId']) in itemIDs):
                        nameAndItems.append((playerJSON['username'], item['contents']['itemId'], item['contents']['quantity']))
        
    return nameAndItems
if(__name__ == "__main__"):
    checkPlayers([6090004])