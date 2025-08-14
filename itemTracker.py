import asyncio
from discord.ext import commands, tasks
from discord import app_commands
import discord
import requests
import json
import re
import codex, contribution
from barterStallTracker import stallInventories, itemIdsToName, itemNameToIds
import main
from shared import contribution_msg_list, trackedItemsAndAmount
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
BOT_TOKEN= open("botToken").read()
HELP_MESSAGE = open("help.txt").read()

taskIds = {}
MAX_TASK = 50
# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.send(error)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Check starting inventory")

# Create a slash command group for /track
track_group = app_commands.Group(name="track", description="Track-related commands")

@track_group.command(name="refined", description="Start tracking a refined item.")
async def track_refined(
    ctx,
    item: str,
    tier: app_commands.Range[int, 1, 9]
):
    channel = bot.get_channel(ctx.channel.id)
    await refined(ctx, item, tier, channel)

@track_group.command(name="stop", description="Stop tracking a task.")
async def track_stop(
    ctx,
    taskid: int
):
    await stopTask(ctx, taskid)

@track_group.command(name="help", description="Show help for tracking commands.")
async def track_help(
    ctx
):
    channel = bot.get_channel(ctx.channel.id)
    await help(ctx, channel)

# Add the group to the bot's tree
bot.tree.add_command(track_group)


    
# @track_refined.autocomplete("cmd")
# async def cmd_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
#     options = ['refined', 'help']
#     return [app_commands.Choice(name=option, value=option) for option in options if option.lower().startswith(current.lower())][:25]
@track_refined.autocomplete("item")
async def item_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    options = ['cloth', 'planks', 'bricks', 'journals', 'ingots', 'leather']
    return [app_commands.Choice(name=option, value=option) for option in options if option.lower().startswith(current.lower())][:25]

async def help(ctx, channel):
    await channel.send(HELP_MESSAGE)
        
    
async def init(channel, message, resources, all):
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
            if (send_contribution_msg.is_running()):
                task = bot.loop.create_task(print_inventories_loop(channel, message, resources, i))
                taskIds[i] = [task, message, resources]

            else:
                task = bot.loop.create_task(print_inventories_loop(channel, message, resources, i))
                taskIds[i] = [task, message, resources]

                bot.loop.create_task(asyncio.to_thread(main.start))
                send_contribution_msg.start(channel)
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
    resources = taskIds[taskID][2]
    for item in resources:
        if item in trackedItemsAndAmount and resources[item][1] != trackedItemsAndAmount[item][1]:
            trackedItemsAndAmount[item][1] = trackedItemsAndAmount[item][1] - resources[item][1]
        else:
            trackedItemsAndAmount.pop(item)
    await taskIds[taskID][1].delete()
    await ctx.response.send_message("Task cancelled", ephemeral=True)
    taskIds.pop(taskID)

async def refined(ctx, item, tier, channel):
    acceptedItems = ["cloth", "leather", "planks", "ingots", "bricks", "journals"]
    try:
        int(tier)
    except:
        await ctx.send("Incorrect tier syntax")
        return
    if (item.lower() not in acceptedItems or int(tier) >= 10 or int(tier) < 1):
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
        await ctx.response.send_message("Processing...", ephemeral=True)
        message = await channel.send("Starting tracking...")
        for item in resources.keys():
            if item not in trackedItemsAndAmount:
                trackedItemsAndAmount[item] = resources[item]
            elif item in trackedItemsAndAmount:
                trackedItemsAndAmount[item] = trackedItemsAndAmount[item] + resources[item]
        await init(channel,message, resources, True)
    

async def print_inventories_loop(channel, message, trackedItemsAndAmountLocal, taskID, stallID=0):
    id_sent = False
    while True:
        finalMsg = ""
        cnt = 0
        prevTier = 1

        for item in trackedItemsAndAmountLocal.keys():
            try:
                trackedItemsAndAmountLocal[item] = [
                    stallInventories[item],
                    trackedItemsAndAmountLocal[item][1],
                    trackedItemsAndAmountLocal[item][2]
                ]
            except:
                pass

        for item, amounts in trackedItemsAndAmountLocal.items():
            if len(amounts) == 3:
                currTier = amounts[2][1]
                if int(currTier) != prevTier:
                    finalMsg += f"\n\n**`{amounts[2]}: {amounts[0]}/{amounts[1]}`**"
                else:
                    finalMsg += f"\n**`{amounts[2]}: {amounts[0]}/{amounts[1]}`**"
                trackedItemsAndAmount[item] = [0, amounts[1], amounts[2]]
                cnt += 1
                prevTier = int(currTier)
            else:
                finalMsg += f"\n`{itemIdsToName[item]}: {amounts[0]}/{amounts[1]}`"
                trackedItemsAndAmount[item] = [0, amounts[1]]

        # finalMsg += f"\nTask ID: {taskID}"
        if not id_sent:
            await channel.send(f"\nTask ID: {taskID}")
            id_sent = True
        await message.edit(content=finalMsg)

        await asyncio.sleep(2)

        
                    
    
if (__name__ == "__main__"):
    
    bot.run(BOT_TOKEN)