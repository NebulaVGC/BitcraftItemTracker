import ast
import json
contribution_msg_list = []
items = open('item.json').read()
items = ast.literal_eval(items)
itemIdsToName = {}
for i in items:
    temp = json.loads(i)
    itemIdsToName[temp['id']] = temp['name'].lower()
    

players = open('players.txt').read()
players = ast.literal_eval(players)
playerIdsToName = {}
for i in players:
    temp = json.loads(i)
    playerIdsToName[temp['player_entity_id']] = temp['user_name']
itemNameToIds = {}
for i in items:
    temp = json.loads(i)
    itemNameToIds[temp['name'].lower()] = temp['id']
trackedItemsAndAmount = {}