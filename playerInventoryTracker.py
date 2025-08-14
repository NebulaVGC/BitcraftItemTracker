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

items = open('item.json').read()
items = ast.literal_eval(items)
itemIdsToName = {}
for i in items:
    temp = json.loads(i)
    itemIdsToName[temp['id']] = temp['name'].lower()
    

# players = open('players.txt').read()
# players = ast.literal_eval(players)
playerIdsToName = {}
players = []
# for i in players:
#     temp = json.loads(i)
#     playerIdsToName[temp['player_entity_id']] = temp['user_name']
    
    

def main():
    inventories = {}
    uri = '{scheme}://{host}/v1/database/{module}/{endpoint}'
    proto = Subprotocol('v1.json.spacetimedb')
    host = "bitcraft-early-access.spacetimedb.com"
    module = "bitcraft-9"
    auth = open("bitcraft-auth.txt").read()
    while (1):
        try:
            with connect(
                    uri.format(scheme='wss', host=host, module=module, endpoint='subscribe'),
                    # user_agent_header=None,
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
                            f"SELECT * FROM claim_member_state WHERE claim_entity_id = 648518346353424439"
                        
                    ]
                )))
                ws.send(sub)
                for msg in ws:
                        data = json.loads(msg)
                        if ('InitialSubscription' in data):
                            for i in data['InitialSubscription']['database_update']['tables'][0]['updates'][0]['inserts']:
                                    temp = json.loads(i)
                                    players.append(temp['player_entity_id'])
                                    playerIdsToName[temp['player_entity_id']] = temp['user_name']
                                    #print(temp['player_entity_id'])
                        else:
                            # for i in data['TransactionUpdate']['status']['Committed']['tables'][0]['updates'][0]['inserts']:

                            #     temp = json.loads(i)
                            print(data)
                        break
                            
                        
        except Exception as e:
            print(e)
        
        
        
        
        try:
            ids = []
            for id in playerIdsToName.keys():
                ids.append(id)
            conditions = " OR ".join(f"owner_entity_id = {i}" for i in ids)
            with connect(
                    uri.format(scheme='wss', host=host, module=module, endpoint='subscribe'),
                    # user_agent_header=None,
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
        #                 f'SELECT * FROM {q};' if isinstance(q, str) else
        #                 f'SELECT * FROM {q[0]} WHERE {q[1]} = {q[2]};'
                            f"SELECT * FROM inventory_state WHERE {conditions}",
                            f"SELECT * FROM claim_member_state WHERE claim_entity_id = 648518346353424439"
                            #"SELECT c1.* FROM claim_member_state c1 JOIN claim_state c2 ON c1.claim_entity_id = c2.entity_id WHERE c2.name = 'CSB Port Oriel'"
                        #for q in queries
                        
                    ]
                )))
                ws.send(sub)
                for msg in ws:
                        data = json.loads(msg)
                        # with open("inventory.json", "w") as f:
                        #     f.write(str(data))
                        if ("InitialSubscription" in data and data['InitialSubscription']['database_update']['tables'][0]['table_name'] == "inventory_state"):
                            for i in data['InitialSubscription']['database_update']['tables'][0]['updates'][0]['inserts']:
                                temp = json.loads(i)
                                handleInitialSub(temp, inventories)
                            tempInv = {}
                            for id in inventories:
                                
                                for item in inventories[id][0]:
                                    try:
                                        if(id in tempInv):
                                            tempInv[id].append((itemIdsToName[item[1][1][0]], item[1][1][1]))
                                        else:
                                            tempInv[id] = [(itemIdsToName[item[1][1][0]], item[1][1][1])]
                                        pass
                                    except:
                                        pass
                            inventories = tempInv
                        elif ('TransactionUpdate' in data and data['TransactionUpdate']['status']['Committed']['tables'][0] == 'claim_member_state'):
                            break
                        else:
                            # with open("inventory2.txt", "w") as f:
                            #     f.write(str(data))
                            for i in data['TransactionUpdate']['status']['Committed']['tables'][0]['updates'][0]['inserts']:

                                temp = json.loads(i)
                                handleOthersSub(temp, inventories)
            
        except Exception as e:
            print(traceback.format_exc())
        
def handleInitialSub(invData, inventories):

    if(invData['owner_entity_id'] in inventories):
        if (invData['inventory_index'] == 0):
            inventories[invData['owner_entity_id']].insert(0,invData['pockets'])
    else:
        if (invData['inventory_index'] == 0):
            inventories[invData['owner_entity_id']] = [invData['pockets']]

def sum_quantities(inv):
    totals = defaultdict(int)
    for item_name, qty in inv:
        totals[item_name] += qty
    return totals

def handleOthersSub(invData, inventories):
    id = invData[4]
    inventory_index = invData[2]
    if id in inventories and inventory_index == 0:
        prevInv = inventories[id]  # list of (item_name, qty) tuples
        currData = invData[1]
        currInv = []
        
        for item in currData:
            try:
                currInv.append((itemIdsToName[item[1][1][0]], item[1][1][1]))
            except:
                pass

        prev_totals = sum_quantities(prevInv)
        curr_totals = sum_quantities(currInv)

        all_items = set(prev_totals.keys()).union(curr_totals.keys())

        for item in all_items:
            prev_qty = prev_totals.get(item, 0)
            curr_qty = curr_totals.get(item, 0)
            diff = curr_qty - prev_qty
            
            if diff < 0:
                on_inventory_change("player", item, diff,playerIdsToName[id] )
            elif diff > 0:
                on_inventory_change("player", item, diff,playerIdsToName[id])
        # Update the stored inventory with current snapshot
        inventories[id] = currInv
            

if (__name__ == "__main__"):
    main()