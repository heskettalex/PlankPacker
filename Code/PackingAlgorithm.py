from Plank import Plank
import math

def packCuts(cuts, order_lengths, inventory=None):
    packedCuts = {key: None for key in cuts}
    for category in packedCuts:
        packedCuts[category] = []
        packedCuts[category].append(Plank(order_lengths[category][0]))
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
                newPlank = None
                for length in order_lengths[category]:
                    if cut_length <= length:
                        newPlank = Plank(length)
                        break
                if newPlank is None:
                    raise Exception(f"Cut {cut_length}\" in category {category[0]}x{category[1]} is too large for order length {order_lengths[category][len(order_lengths[category]) - 1]}\"")
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
