import os

def readCutList(inputFile):
    cutsDict = {}
    currentCategory = ""

    with open(inputFile) as file:
        for line_num, l in enumerate(file, start=1):
            line = l.strip()
            if len(line) == 0:
                continue
            try:
                if line[-1] == ":":
                    category = (int(line[0 : line.index("x")]), int(line[line.index("x") + 1 : line.index(":")]))
                    if category not in cutsDict:
                        cutsDict[category] = []
                    currentCategory = category  
                else:
                    count = int(line[0 : line.index("x")])
                    measurement = float(line[line.index("x") + 2 :])
                    for _ in range(count):
                        cutsDict[currentCategory].append(measurement)
            except Exception as e:
                raise Exception(f"Error on line {line_num}: \"{line}\", {e}")
    numCategories = len(cutsDict)
    numCuts = 0
    for c in cutsDict.values():
        numCuts += len(c) - 2
    for key in cutsDict:
        cutsDict[key] = sorted(cutsDict[key], reverse=True)
    
    print(f"\nImported cut list \"{os.path.basename(inputFile)}\"\n{numCategories} categories, {numCuts} cuts\n")
    
    sorted_categories = dict(sorted(cutsDict.items(), key=lambda cat: (cat[0], cat[1])))
    return sorted_categories