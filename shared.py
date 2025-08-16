import ast
import json
contribution_msg_list = []
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
trackedItemsAndAmount = {}