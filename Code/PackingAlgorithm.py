from Plank import Plank
import math

def packCuts(cuts, orderLength, overflowIncrement, inventory=None): #cuts are ordered greatest to least
    packedCuts = {key: None for key in cuts}

    for category in packedCuts:
        packedCuts[category] = []
        packedCuts[category].append(Plank(orderLength))
        try:
            for length, note in inventory[category]:
                inventoryPlank = Plank(length, note, True)
                packedCuts[category].append(inventoryPlank)
        except Exception:
            pass

        packedCuts[category].reverse()

        for cut_length, note in cuts[category]:
            placed = False
            for plank in packedCuts[category]:
                try:
                    plank.addCut((cut_length, note))
                    placed = True
                    break
                except ValueError:
                    continue
            if not placed:
                if cut_length > orderLength:
                    newPlank = Plank(math.ceil((cut_length - orderLength) / overflowIncrement) * overflowIncrement + orderLength)
                else:
                    newPlank = Plank(orderLength)
                newPlank.addCut((cut_length, note))

                inserted = False
                for i in range(len(packedCuts[category])):
                    if packedCuts[category][i].freeStock() > newPlank.freeStock():
                        packedCuts[category].insert(i, newPlank)
                        inserted = True
                        break
                
                if not inserted:
                    packedCuts[category].append(newPlank)
        
        packedCuts[category] = [plank for plank in packedCuts[category] if len(plank.cuts) > 0]
        packedCuts[category].sort(key=lambda plank: -plank.length)   
    
    return packedCuts
