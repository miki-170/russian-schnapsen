from enum import Enum


# Classes for the mechanics - Cards

class Rank(Enum):
    NINE = ("9",0)
    TEN = ("10",10)
    JACK = ("J",2)
    QUEEN = ("Q",3)
    KING = ("K",4)
    ACE = ("A",11)

    def __init__(self,display,points):
        self.display = display
        self.points = points

class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit

    @property
    def points(self):
        return self.rank.points

    # used repr instead of 
    def __repr__(self):
        return f"{self.rank.display}{self.suit.value}"
    
    # function checking if the card is trump 
    def is_kozyr(self,trump_suit):
        return self.suit == trump_suit
    
    # function checking equality
    def __eq__(self, other):
        return isinstance(self,Card) and self.rank == other.rank and self.suit == other.suit
    
    # hashing the same cards to the same address, so we do not create separate addresses for the same cards

    def __hash__(self):
        return hash((self.rank,self.suit))
    

# Deck 

class Deck:
    pass


king_of_hearts = Card(Rank.KING, Suit.HEARTS)

print(king_of_hearts)

