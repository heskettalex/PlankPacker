from collections import Counter
from Utils import value_to_frac

class Plank:
    def __init__(self, length: float, inventory: bool = False):
        self.length = length
        self.inventory = inventory
        self.cuts = []
    
    def freeStock(self):
        return self.length - sum(self.cuts)
    
    def addCut(self, cut: float):
        if cut > self.freeStock():
            raise ValueError(f"Cut {cut} is too long for plank of length {self.length}.")
        self.cuts.append(cut)

    def __str__(self):
        counts = Counter(self.cuts)
        return "+ ".join(f"{count}x {value_to_frac(cut)}\"" for cut, count in counts.items())
    
    def __eq__(self, other):
        if not isinstance(other, Plank):
            return False
        return self.length == other.length and self.cuts == other.cuts and self.inventory == other.inventory
    
    def __hash__(self):
        return hash((self.length, tuple(self.cuts)))