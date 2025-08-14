import asyncio
from discord.ext import commands, tasks
import discord
import requests
import json
import re
import codex, contribution
from barterStallTracker import stallInventories, itemIdsToName, itemNameToIds
import main
from shared import contribution_msg_list
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
BOT_TOKEN= open("botToken").read()
HELP_MESSAGE = open("help.txt").read()

taskIds = {}
MAX_TASK = 50
# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.send(error)


@bot.event
async def on_ready():
    print("Check starting inventory")
    
@bot.command()
async def track(ctx,*arr):
    channel = bot.get_channel(ctx.channel.id)
    if (arr[0] == "start"):
        await start(ctx, channel, *arr)
    elif (arr[0] == "stop"):
        await stopTask(ctx, (int(arr[1])))
    elif (arr[0] == "all"):
        print("all")
    elif (arr[0] == "refined"):
        await refined(ctx, arr[1], arr[2], channel)
    elif (arr[0] == "help"):
        await help(ctx, channel)
    else: 
        await ctx.send("Unknown keyword")

async def help(ctx, channel):
    await channel.send(HELP_MESSAGE)
        
    
async def init(channel, message, trackedItemsAndAmount, all):
    # if (all == True):
    #     stallID = 0
    # else:
    #     for building in bldgJSON:
    #             if ("Barter Stall" in building['buildingName']):
    #                 for item in building['inventory']:
    #                     itemID = item['contents']['item_id']
    #                     itemQuantity = item['contents']['quantity']
    #                     if (itemID == 11001 and itemQuantity == 3):
    #                         stallID = building['entityId']
    #                         found = 1
    #     if(found == 0):          
    #         await channel.send("Sticks not found")
    #         return
    i = 1
    iters = 0
    while(1):
        if(i in taskIds):
            i += 1
            iters += 1
        else:
            #taskIds[i] = [bot.loop.create_task(checkStall(trackedItemsAndAmount, stallID, message, i)), message]
            printInventories.start(trackedItemsAndAmount, message, i)
            bot.loop.create_task(asyncio.to_thread(main.start, trackedItemsAndAmount))
            send_contribution_msg.start(channel)
            #await checkPlayers(trackedItemsAndAmount)
            break
        if (iters >= MAX_TASK):
            await channel.send("Max tasks reached")
            return
@tasks.loop(seconds=2, count=None)
async def send_contribution_msg(channel):
        if contribution_msg_list:
            for msg in contribution_msg_list:
                await channel.send(msg)
            contribution_msg_list.clear()
        
async def start(ctx, channel, *arr):
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
        if (item not in itemNameToIds):
            print("Unknown item")
            return
        trackedID = itemNameToIds[item]
        trackedItemsAndAmount[trackedID] = [0,amount]
    message = await channel.send("Starting tracking...")
    await init(stallInventories, channel,message, trackedItemsAndAmount, False)
    
            
async def stopTask(ctx, taskID):
    taskIds[taskID][0].cancel()
    await taskIds[taskID][1].delete()
    taskIds.pop(taskID)
    await ctx.send("Task cancelled")

async def refined(ctx, item, tier, channel):
    acceptedItems = ["cloth", "leather", "planks", "ingots", "bricks", "journals"]
    try:
        int(tier)
    except:
        await ctx.send("Incorrect tier syntax")
        return
    if (item.lower() not in acceptedItems or int(tier) >= 10):
        await ctx.send("Incorrect item or tier syntax")
    else:
        if(item == "cloth"):
            resources = codex.getCloth(tier, itemNameToIds)
        elif(item == "leather"):
            resources = codex.getLeather(tier, itemNameToIds)
        elif(item == "ingots"):
            resources = codex.getIngots(tier, itemNameToIds)
        elif(item == "planks"):
            resources = codex.getPlanks(tier, itemNameToIds)
        elif(item == "bricks"):
            resources = codex.getBricks(tier, itemNameToIds)
        elif(item == "journals"):
            resources = codex.getJournals(tier, itemNameToIds)
        message = await channel.send("Starting tracking...")
        await init(channel,message, resources, True)
    

@tasks.loop(seconds=2, count=None)
async def printInventories(trackedItemAndAmount, message, taskID, stallID=0):
    finalMsg = ""
    cnt = 0
    prevTier = 1
    for item in trackedItemAndAmount.keys():
        try:
            trackedItemAndAmount[item] = [stallInventories[item],trackedItemAndAmount[item][1],trackedItemAndAmount[item][2]]
        except Exception as e:
            pass
    for item,amounts in trackedItemAndAmount.items():
        if (len(amounts) == 3):    
            currTier = amounts[2][1]
            if (int(currTier) != prevTier):
                finalMsg = finalMsg + "\n\n**`" + amounts[2] + ": " + str(amounts[0]) + "/" + str(amounts[1]) + "`**"
            else: 
                finalMsg = finalMsg + "\n**`" + amounts[2] + ": " + str(amounts[0]) + "/" + str(amounts[1]) + "`**" 
            trackedItemAndAmount[item] = [0, amounts[1], amounts[2]]
            cnt += 1
            prevTier = int(currTier)
            
        else:
            finalMsg = finalMsg + "\n`" + itemIdsToName[item] + ": " + str(amounts[0]) + "/" + str(amounts[1]) + "`" 
            trackedItemAndAmount[item] = [0, amounts[1]]
    finalMsg = finalMsg + f"\nTask ID: {taskID}"
    await message.edit(content=finalMsg)
        
                    
    
if (__name__ == "__main__"):
    bot.run(BOT_TOKEN)