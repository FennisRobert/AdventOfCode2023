from aoc import *
from collections import defaultdict
hands = load(7,2023,False).findgroups('([AKQJT98765432]{5}) (\d+)')

CARDS = [c for c in 'AKQT98765432J']
CARDV = {c: i for i,c in enumerate(CARDS[::-1])}
print(CARDV)

class Hand:
    
    def __init__(self, hand: str, bet: str, check=True):
        self.hand = hand
        self.counts = {c: self.hand.count(c) for c in CARDS}
        self.nin = set(self.counts.values())
        self.ncounts = {N: sum([n==N for c,n in self.counts.items()]) for N in [0,1,2,3,4,5]}
        self.bet = int(bet)
        if check:
            self.handrank = self._shandrank
        else:
            self.handrank = self._handrank
    
    def __str__(self) -> str:
        return f'Hand({self.hand},{self.handrank},{self.bet})'
    
    @property
    def fiveoak(self):
        return 5 in self.nin
    
    @property
    def fouroak(self):
        return 4 in self.nin
    
    @property
    def fullhouse(self):
        return (3 in self.nin) and (2 in self.nin)
    
    @property
    def threeoak(self):
        return (3 in self.nin) and self.ncounts[1]==2
    
    @property
    def twopair(self):
        return (2 in self.nin) and (1 in self.nin) and self.ncounts[2]==2
    
    @property
    def onepair(self):
        return self.ncounts[2]==1 and self.ncounts[1]==3
    
    @property
    def highcard(self):
        return self.counts[1]==5
    
    @property
    def _shandrank(self) -> float:
        return max([Hand(self.hand.replace('J',c),0,False)._handrank for c in CARDS])
    
    @property
    def _handrank(self) -> float:
        if self.fiveoak:
            return 6
        if self.fouroak:
            return 5
        if self.fullhouse:
            return 4
        if self.threeoak:
            return 3.5
        if self.twopair:
            return 3
        if self.onepair:
            return 2
        return 1
    
    def __lt__(self, other):
        if self.handrank<other.handrank:
            return True
        if self.handrank>other.handrank:
            return False
        for c1, c2 in zip(self.hand, other.hand):
            if CARDV[c1] < CARDV[c2]:
                return True
            if CARDV[c2] < CARDV[c1]:
                return False
        return False


    
Hands = [Hand(*h.items[0]) for h in hands]

SortedHands = sorted(Hands,reverse=False)
#print([str(h) for h in sorted(SortedHands)])
Value = [(i+1)*h.bet for i,h in enumerate(SortedHands)]
print(sum(Value))
