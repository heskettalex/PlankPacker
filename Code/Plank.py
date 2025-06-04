from collections import Counter
from Utils import value_to_frac

class Plank:
    def __init__(self, length: float, note: str="", inventory: bool = False):
        self.length = length
        self.inventory = inventory
        self.cuts = []
        self.note = note
    
    def freeStock(self):
        sum = 0
        for cut in self.cuts:
            sum += cut[0]
        return self.length - sum
    
    def addCut(self, cut: tuple):
        if cut[0] > self.freeStock():
            raise ValueError(f"Cut {cut[0]}\" is too long for plank of length {self.length}\".")
        self.cuts.append(cut)

    def __str__(self):
        counts = Counter(self.cuts)
        output = ""
        first = True
        for cut, count in counts.items():
            if first:
                first = False
            else:
                output += " + "
            if cut[1] == "":
                output += f"{count}x {value_to_frac(cut[0])}\""
            else:
                output += f"{count}x {value_to_frac(cut[0])}\" ({cut[1]})"
        return output
    
    def __eq__(self, other):
        if not isinstance(other, Plank):
            return False
        return self.length == other.length and self.cuts == other.cuts and self.inventory == other.inventory
    
    def __hash__(self):
        return hash((self.length, tuple(self.cuts)))