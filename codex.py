tierToName = {}
tierToName[1] = "rough"
tierToName[2] = "simple"
tierToName[3] = "sturdy"
tierToName[4] = "fine"
tierToName[5] = "exquisite"
tierToName[6] = "peerless"
tierToName[7] = "ornate"
tierToName[8] = "pristine"
tierToName[9] = "magnificent"
tierToName[10] = "flawless"


def getCloth(tier):
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
            finalResources[item.replace(f"T{i}", tierToName[i])] = resources[item]        
            if (item in finalResources):
                finalResources.pop(item)
    return finalResources
    