from enum import Enum
import random


# Classes for the mechanics - Cards

class Rank(Enum):
    NINE = ("9",0)
    JACK = ("J",2)
    QUEEN = ("Q",3)
    KING = ("K",4)
    TEN = ("10",10)
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
    
    # function checking if the card is trump (kozyr is a polish name for a trump card)
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

    def __init__(self):
        self.cards: list[Card] = []
        self.build()

    def build(self):
        self.cards = [Card(rank,suit) for rank in Rank for suit in Suit]
    
    
    def shuffle(self):
        random.shuffle(self.cards)
        return self
    
    @property
    def top_card(self):
        return self.cards[0] if self.cards else None
    
    def deal(self,n=1):
        if n > len(self.cards):
            raise ValueError(f"Only {len(self.cards)} cards left in the deck.")
        else:
            dealt = self.cards[:n]
            self.cards=self.cards[n:]
            return dealt

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Full deck: {self.cards}"


# Players' hands

trump_points= {
    Suit.SPADES :40 ,
    Suit.CLUBS :60 ,
    Suit.DIAMONDS :80 ,
    Suit.HEARTS :100 
}


class Hand:

    def __init__(self):
        self.cards = []
        
    def sort(self):
        self.cards.sort(key= lambda c: (c.suit.value , c.rank.points))

    def add(self,cards):
        self.cards.extend(cards)
        self.sort()
    
    def remove(self,card):
        self.cards.remove(card)

    # function checking if hand contains a marriage of the given suit
    def has_marriage(self, suit):
        suit_cards = [c for c in self.cards if c.suit == suit]
        ranks = [x.rank for x in suit_cards]    
        return Rank.KING in ranks and Rank.QUEEN in ranks

    # function listing all the marriages
    def marriages(self):
        return [suit for suit in Suit if self.has_marriage(suit)]

    def get_limit(self):
        lim =120
        for suit in self.marriages():
            lim += trump_points[suit]
        return min(lim,360)

    # return the list of cards that can be played
    def legal_moves(self,trump,count,lead_card= None):

        # if you start there is no constraints
        if lead_card is None or count ==2:
            return list(self.cards)

        # following the suit of the top card
        same_suit = [c for c in self.cards if c.suit == lead_card.suit ]
        suit_better = [c for c in same_suit if c.points > lead_card.points]
        if suit_better:
            return suit_better
        if same_suit:
            return same_suit
        
        # now if we have the trump we have to play it

        trump_cards = [c for c in self.cards if c.is_kozyr(trump)]

        if trump_cards:
            return trump_cards
        
        # if none of those work just play anything

        return list(self.cards)

    # enables to call len() on an instance
    def __len__(self):
        return len(self.cards)
    
    #gives a nice print of an instance
    def __repr__(self):
        return f"The hand is {' , '.join(repr(c) for c in self.cards)}"


