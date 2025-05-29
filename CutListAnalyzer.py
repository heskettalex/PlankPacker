import math
from Plank import Plank
from collections import Counter
def stats(cuts , orderLength, overflowIncrement):
    totalLength = 0.0
    totalWaste = 0.0
    totalCuts = 0
    inventoryCuts = 0
    maxWaste = 0.0

    for category in cuts:
        for plank in cuts[category]:
            totalLength += plank.length
            totalWaste += plank.freeStock()
            if plank.inventory:
                inventoryCuts += len(plank.cuts)
            totalCuts += len(plank.cuts)
            for cut in plank.cuts:
                if cut > orderLength:
                    maxWaste += math.ceil(cut / overflowIncrement) * overflowIncrement - cut
                else:
                    maxWaste += orderLength - cut

    return f"Waste reduced by {(1 - totalWaste / maxWaste) * 100:.1f}%\n\nWaste: {totalWaste / totalLength * 100:.1f}%\nInventory utilization: {inventoryCuts / totalCuts * 100:.1f}%"

def summary(cuts):
    order = "Additional Stock Needed:\n"

    for category in cuts:
        planks = []
        for plank in cuts[category]:
            planks.append(Plank(plank.length, plank.inventory))
        
        thickness, width = category
        category_label = f"{thickness}x{width}:\n"

        has_order = any(not plank.inventory for plank in planks)
        if has_order:
            order += category_label

        plank_counter = Counter(planks)
        for plank, count in plank_counter.items():
            line = f" - {count}x {plank.length}\"\n"
            if not plank.inventory:
                order += line


    if order == "Additional Needed:\n":
        return "No additional stock needed."
    return order

def printCuts(cuts):
    output = "Cut List Instructions:\n(* = from inventory)\n"
    for category in cuts:
        thickness, width = category
        output += f"{thickness}x{width}:\n"
        plank_counter = Counter(cuts[category]).most_common()

        inventory = ""
        order = ""
        for plank, count in plank_counter:
            line = f"{count}x {plank.length}\" => "

            if len(plank.cuts) == 1:
                cut = plank.cuts[0]
                line += f"{count}x {cut}\""
            else:
                if count > 1:
                    line += f"{count}x ({plank})"
                else:
                    line += f"{plank}"

            if plank.inventory:
                line = "*" + line
                inventory += f" - {line}\n"
            else:
                order += f" - {line}\n"
        output += order + inventory
    return output
