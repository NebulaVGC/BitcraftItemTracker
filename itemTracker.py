from discord.ext import commands, tasks
import discord
import requests
import json
import re
import codex
import time
CHANNEL_ID = 701225984824705047
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
BOT_TOKEN= open("botToken").read()

taskIds = {}
MAX_TASK = 50

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


def getAndParseData():
    raw = requests.get('https://bitjita.com/claims/648518346353424439#inventories').text
    start = raw.find("buildings:")
    bldgRaw = raw[raw.find("buildings:", start + 1) +11: -24]
    bldgRaw = (bldgRaw[:bldgRaw.find("inventories:") - 2])
    itemRaw = bldgRaw
    bldgRaw = bldgRaw[:bldgRaw.find("items:") - 1]
    itemRaw = itemRaw[itemRaw.find("items:") + 7:itemRaw.find("cargos:")-2]

    bldgRaw = bldgRaw.strip()
    bldgRaw = bldgRaw.rstrip(',')
    bldgRaw = '[' + bldgRaw
    bldgRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', bldgRaw)
    bldgRaw = bldgRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')

    bldgJSON = json.loads(bldgRaw)

    itemRaw = itemRaw.strip()
    itemRaw = itemRaw.rstrip(',')
    itemRaw= '[' + itemRaw + ']'
    itemRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', itemRaw)
    itemRaw = itemRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')
    itemJSON = json.loads(itemRaw)
    
    return bldgJSON, itemJSON

def getAllItems():
    raw = requests.get('https://bitjita.com/items').text
    start = raw.find("items:")
    fin = raw[start:]
    fin = fin.find("metrics:")
    itemRaw = raw[start +7: start + fin -1]
    itemRaw = itemRaw.strip()
    itemRaw = itemRaw.rstrip(',')
    itemRaw= '[' + itemRaw 
    itemRaw = re.sub(r'([{,])(\s*)([A-Za-z_]\w*):', r'\1"\3":', itemRaw)
    itemRaw = itemRaw.replace('false', 'false').replace('true', 'true').replace('null', 'null')
    itemRaw = re.sub(r'(?<!\d)\.(\d)', r'0.\1', itemRaw)
    itemJSON = json.loads(itemRaw)
    return itemJSON


@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Tracking bot is ready")
    
@bot.command()
async def track(ctx,*arr):
    if (arr[0] == "start"):
        await start(ctx, *arr)
    elif (arr[0] == "stop"):
        await stopTask(ctx, (int(arr[1])))
    elif (arr[0] == "all"):
        print("all")
    elif (arr[0] == "refined"):
        await refined(ctx, arr[1], arr[2])
    else: 
        await ctx.send("Unknown keyword")
        
    
    

async def start(ctx, *arr):
    channel = bot.get_channel(ctx.channel.id)
    i = 1
    trackedItemsAndAmount = {}
    while (i < len(arr) - 1):
        try:
            int(arr[i+1])
        except ValueError:
            await channel.send("Invalid quantity")
            break
        item = arr[i].lower()
        amount = arr[i+1]
        i = i+2
        if (item not in nameIDs):
            print("Unknown item")
            break
        trackedID = nameIDs[item]
        bldgJSON, itemJSON = getAndParseData()
        found = 0
        for building in bldgJSON:
                if ("Barter Stall" in building['buildingName']):
                    for item in building['inventory']:
                        itemID = item['contents']['item_id']
                        itemQuantity = item['contents']['quantity']
                        if (itemID == 11001 and itemQuantity == 3):
                            stallID = building['entityId']
                            found = 1
        if(found == 0):          
          await channel.send("Sticks not found")
          break
        trackedItemsAndAmount[trackedID] = [0,amount]
    message = await channel.send("Starting tracking...")
    i = 1
    iters = 0
    while(1):
        if(i in taskIds):
            i += 1
            iters += 1
        else:
            taskIds[i] = bot.loop.create_task(checkStall(trackedItemsAndAmount, stallID, message))
            await channel.send(f"TaskID: {i}")
            break
        if (iters >= MAX_TASK):
            print("MAX TASKS REACHED")
            return
            
async def stopTask(ctx, taskID):
    taskIds[taskID].cancel()
    await ctx.send("Task cancelled")

async def refined(ctx, item, tier):
    acceptedItems = ["cloth", "leather", "planks", "ingots", "bricks", "Journals"]
    try:
        int(tier)
    except:
        await ctx.send("Incorrect tier syntax")
        return
    if (item.lower() not in acceptedItems or int(tier) >= 10):
        await ctx.send("Incorrect item or tier syntax")
    else:
        resources = codex.getCloth(tier)
        
    

    
@tasks.loop(seconds=10, count=None)
async def checkStall(trackedItemAndAmount, stallID, message):
    channel = bot.get_channel(CHANNEL_ID)
    bldgJSON, itemJSON = getAndParseData()
    for building in bldgJSON:
        if (building['entityId'] == stallID):
            for item in building['inventory']:
                itemID = str(item['contents']['item_id'])
                if itemID in trackedItemAndAmount:
                    currAmount = item['contents']['quantity'] + trackedItemAndAmount[itemID][0]
                    limit = trackedItemAndAmount[itemID][1]
                    trackedItemAndAmount[itemID] = [currAmount, limit]
    finalMsg = ""
    for item,amounts in trackedItemAndAmount.items():
        finalMsg = finalMsg + "\n" + itemIDs[item] + ":" + str(amounts[0]) + "/" + str(amounts[1]) 
        trackedItemAndAmount[item] = [0, amounts[1]]
    await message.edit(content=finalMsg)
        
                    
# Item ID -> item name    
itemIDs = {}
# Item name -> item ID
nameIDs = {}
    
if (__name__ == "__main__"):

    itemJSON = getAllItems()
    for item in itemJSON:
        if item['id'] not in itemIDs:
            itemIDs[item['id']] = item['name'].lower()
        if item['name'] not in nameIDs:
            nameIDs[item['name'].lower()] = item['id']
    bot.run(BOT_TOKEN)