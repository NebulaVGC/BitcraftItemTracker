tierToName = {}
tierToName[1] = "rough"
tierToName[2] = "simple"
tierToName[3] = "sturdy"
tierToName[4] = "fine"
tierToName[5] = "exquisite"
tierToName[6] = "peerless"
tierToName[7] = "ornate"
tierToName[8] = "pristine"
tierToName[9] = "magnificient"
tierToName[9] = "magnificient"
tierToName[10] = "flawless"

tierToNameAlt2 = {}
tierToNameAlt2[1] = "ferralith"
tierToNameAlt2[2] = "pyrelite"
tierToNameAlt2[3] = "emarium"
tierToNameAlt2[4] = "elenvar"
tierToNameAlt2[5] = "luminite"
tierToNameAlt2[6] = "rathium"
tierToNameAlt2[7] = "aurumite"
tierToNameAlt2[8] = "celestium"
tierToNameAlt2[9] = "umbracite"
tierToNameAlt2[10] = "astralite"


tierToNameAlt3 = {}
tierToNameAlt3[1] = "beginner's"
tierToNameAlt3[2] = "novice"
tierToNameAlt3[3] = "essential"
tierToNameAlt3[4] = "proficient"
tierToNameAlt3[5] = "advanced"
tierToNameAlt3[6] = "comprehensive"
tierToNameAlt3[7] = "ornate"
tierToNameAlt3[8] = "pristine"
tierToNameAlt3[9] = "magnificient"
tierToNameAlt3[10] = "flawless"

tierToNameAlt = {}
tierToNameAlt[1] = "basic"
tierToNameAlt[2] = "simple"
tierToNameAlt[3] = "infused"
tierToNameAlt[4] = "fine"
tierToNameAlt[5] = "exquisite"
tierToNameAlt[6] = "peerless"
tierToNameAlt[7] = "ornate"
tierToNameAlt[8] = "pristine"
tierToNameAlt[9] = "magnificient"
tierToNameAlt[10] = "flawless"


def getCloth(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} cloth"
        resources[newItem] = amount * 5
        newHair = f"T{tier} animal Hair"
        newStraw = f"T{tier} straw"
        resources[newHair] = amount
        resources[newStraw] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources


def getLeather(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} leather"
        resources[newItem] = amount * 5
        newBrax = f"T{tier} braxite"
        newOil = f"T{tier} fish oil"
        resources[newBrax] = amount
        resources[newOil] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("fish oil") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources


def getIngots(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} ingot"
        resources[newItem] = amount * 5
        newCitric = f"T{tier} citric berry"
        newPebbles= f"T{tier} pebbles"
        newVial = f"T{tier} glass vial"
        resources[newCitric] = amount
        resources[newPebbles] = amount * 5
        resources[newVial] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("citric") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                elif (item.find("ingot") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt2[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources
    
def getPlanks(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} plank"
        resources[newItem] = amount * 5
        newBrax = f"T{tier} amber resin"
        newOil = f"T{tier} crop oil"
        newVial = f"T{tier} glass vial"
        resources[newBrax] = amount
        resources[newOil] = amount
        resources[newVial] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("crop oil") >= 0 or item.find("resin") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources

def getBricks(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} brick"
        resources[newItem] = amount * 5
        newGypsite = f"T{tier} gypsite"
        newShells = f"T{tier} crushed shells"
        resources[newGypsite] = amount
        resources[newShells] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("shells") >= 0):
                    tier = item[1]
                    newName = f"crushed {tierToName[int(tier)]} shells".lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources

def getJournals(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} parchment"
        resources[newItem] = amount * 10
        newInk = f"T{tier} ink"
        newCarvings = f"T{tier} stone carvings"
        newVials = f"T{tier} glass vial"
        newPigment = f"T{tier} pigment"
        newFishOil = f"T{tier} fish oil"
        resources[newInk] = amount * 10
        resources[newCarvings] = amount * 5
        resources[newVials] = amount * 15
        resources[newPigment] = amount * 10
        resources[newFishOil] = amount * 25
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("ink") >= 0 or item.find("pigment") >= 0 or item.find("fish oil")) >= 0:
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                elif (item.find("carvings") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt3[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources
def getPlanks(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} plank"
        resources[newItem] = amount * 5
        newBrax = f"T{tier} amber resin"
        newOil = f"T{tier} crop oil"
        newVial = f"T{tier} glass vial"
        resources[newBrax] = amount
        resources[newOil] = amount
        resources[newVial] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("crop oil") >= 0 or item.find("resin") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources

def getBricks(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} brick"
        resources[newItem] = amount * 5
        newGypsite = f"T{tier} gypsite"
        newShells = f"T{tier} crushed shells"
        resources[newGypsite] = amount
        resources[newShells] = amount
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("shells") >= 0):
                    tier = item[1]
                    newName = f"crushed {tierToName[int(tier)]} shells".lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources

def getJournals(tier, nameIDs):
    resources = {}
    finalResources = {}
    tier = int(tier)
    amount = tier * 5
    while (tier > 0):
        newItem = f"T{tier} parchment"
        resources[newItem] = amount * 10
        newInk = f"T{tier} ink"
        newCarvings = f"T{tier} stone carvings"
        newVials = f"T{tier} glass vial"
        newPigment = f"T{tier} pigment"
        newFishOil = f"T{tier} fish oil"
        resources[newInk] = amount * 10
        resources[newCarvings] = amount * 5
        resources[newVials] = amount * 15
        resources[newPigment] = amount * 10
        resources[newFishOil] = amount * 25
        amount = amount * 2
        tier -= 1

    for i in range(1,10):
        for item in resources.keys():
            if(item.find(str(i)) >= 0):
                if (item.find("ink") >= 0 or item.find("pigment") >= 0 or item.find("fish oil")) >= 0:
                    newName = item.replace(f"T{i}", tierToNameAlt[i]).lower()
                elif (item.find("carvings") >= 0):
                    newName = item.replace(f"T{i}", tierToNameAlt3[i]).lower()
                else:
                    newName = item.replace(f"T{i}", tierToName[i]).lower()
                finalResources[nameIDs[newName]] = [0,resources[item], item]        
                if (item in finalResources):
                    finalResources.pop(item)
    return finalResources