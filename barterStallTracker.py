import requests
import json
import os
import re
from pathlib import Path
import ast
import requests
import urllib3.util
import traceback
from collections import defaultdict
from websockets import Subprotocol
from websockets.exceptions import WebSocketException
from websockets.sync.client import connect
on_inventory_change = lambda *args, **kwargs: None  # placeholder
#res = requests.post('https://api.bitcraftonline.com/authentication/request-access-code?email=cwtdawg%40gmail.com')
# res = requests.post("https://api.bitcraftonline.com/authentication/authenticate?email=cwtdawg%40gmail.com&accessCode=Y8XP23")

#stallInventories = {}
items = open('item.json').read()
items = ast.literal_eval(items)
itemIdsToName = {}
for i in items:
    temp = json.loads(i)
    itemIdsToName[temp['id']] = temp['name'].lower()
    
itemNameToIds = {}
for i in items:
    temp = json.loads(i)
    itemNameToIds[temp['name'].lower()] = temp['id']
    
f = open("barterStalls.txt")
barterIds = []
for i in f.readlines():
    barterIds.append(int(i.strip()))
    
stallInventories = {}    

def main():
    uri = '{scheme}://{host}/v1/database/{module}/{endpoint}'
    proto = Subprotocol('v1.json.spacetimedb')
    host = "bitcraft-early-access.spacetimedb.com"
    module = "bitcraft-9"
    auth = open("bitcraft-auth.txt").read()

    
    try:
        idString = " OR ".join(f"b.building_description_id = {i}" for i in barterIds)
        with connect(
                uri.format(scheme='wss', host=host, module=module, endpoint='subscribe'),
                additional_headers={"Authorization": "Bearer " + auth} if auth else {},
                subprotocols=[proto],
                max_size=None,
                max_queue=None,
                ping_interval=1
        ) as ws:
            
            ws.recv()
            sub = json.dumps(dict(Subscribe=dict(
                request_id=1,
                query_strings=[
                        f"SELECT i.* FROM building_state b JOIN inventory_state i ON b.entity_id = i.owner_entity_id WHERE (b.claim_entity_id = 648518346353424439) AND ({idString})",
                    
                ]
            )))
            ws.send(sub)
            initial = True
            for msg in ws:
                    
                    data = json.loads(msg)
                    if (initial == True and "InitialSubscription" in data):
                        for i in data['InitialSubscription']['database_update']['tables'][0]['updates'][0]['inserts']:
                            temp = json.loads(i)
                            handleInitialSub(temp, stallInventories)
                        
                    else:
                        # with open("inventory2.txt", "w") as f:
                        #     f.write(str(data))
                            temp = data['TransactionUpdate']['status']['Committed']['tables'][0]['updates'][0]
                            handleOthersSub(temp, stallInventories)
                            
        
    except Exception as e:
        print(traceback.format_exc())
        
def handleInitialSub(invData, inventories):
    for item in invData['pockets']:
        try:
            currId = item[1][1][0]
            quantity = item[1][1][1]
            if currId not in itemIdsToName:
                continue
            inventories[currId] = inventories.get(currId, 0) + quantity
        except:
            continue
    
def sum_quantities(inv):
    totals = defaultdict(int)
    for item_name, qty in inv:
        totals[item_name] += qty
    return totals

def handleOthersSub(invData, inventories):
    insertInv = {}
    deleteInv = {}
    insertData = invData['inserts']
    deleteData = invData['deletes']
    for pocket in insertData:
        for item in json.loads(pocket)[1]:
            try:
                currId = item[1][1][0]
                currQuantity = item[1][1][1]

                if currId not in itemIdsToName:
                    continue
                if (currId in insertInv):
                    insertInv[currId] = insertInv[currId] + currQuantity
                else:
                    insertInv[currId] = currQuantity
        
            except:
                continue
    for pocket in deleteData:
        for item in json.loads(pocket)[1]:
            try:
                currId = item[1][1][0]
                currQuantity = item[1][1][1]
                if currId not in itemIdsToName:
                    continue
                if (currId in deleteInv):
                    deleteInv[currId] = deleteInv[currId] + currQuantity
                else:
                    deleteInv[currId] = currQuantity
            except:
                continue
    for itemId in insertInv.keys():
        if (itemId not in deleteInv):
            inventories[itemId] = insertInv[itemId]
            on_inventory_change("barter_stall", itemIdsToName[itemId], insertInv[itemId])
        elif(insertInv[itemId] > deleteInv[itemId]):
            inventories[itemId] = inventories[itemId] + insertInv[itemId] - deleteInv[itemId]
            on_inventory_change("barter_stall", itemIdsToName[itemId], insertInv[itemId] - deleteInv[itemId])
        elif (insertInv[itemId] < deleteInv[itemId]):
            inventories[itemId] = inventories[itemId] + insertInv[itemId] - deleteInv[itemId]
            on_inventory_change("barter_stall", itemIdsToName[itemId], insertInv[itemId] - deleteInv[itemId])
    for itemId in deleteInv.keys():
        if (itemId not in insertInv):
            inventories[itemId] = 0
            on_inventory_change("barter_stall", itemIdsToName[itemId], -deleteInv[itemId])
        
if (__name__ == "__main__"):
    main()  