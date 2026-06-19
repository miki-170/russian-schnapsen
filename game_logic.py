from cards import Card,Deck,Hand,Rank, Suit, trump_points
import random


class Gamestate:
    
    def __init__(self):
        self.deck = Deck()  # initialising deck
        self.hands = [Hand(),Hand()]    #players' hands
        self.piles = [Hand(),Hand()]    # initial piles
        self.discarded = []
        self.trump_suit = None  # current trump suit

        self.threshold = 100 # minimum a player starting has to play
        self.bets = [100,100] # values for the betting round

        self.starting_player = random.choice([0,1]) # who starts the round
        self.lead_player = 0    # who starts the trick
        self.current_player = 0 # who is currently playing the card

        self.table = []     # current cards on the table
        self.scores = [0,0] # score in this trick
        self.game_points= [0,0]     # total scores 
        self.phase = 'deal'     # deal -> bid -> play -> finished
        

    def start_new_round(self):
        self.deck = Deck()
        # shuffle the deck
        self.deck.shuffle()

        # reset all
        self.hands = [Hand(),Hand()]   
        self.piles = []  
        self.trump_suit = None
        self.bets = [100,100]
        self.scores = [0,0]
        self.anounced_marriages = [] 
        self.phase = 'deal'
        self.starting_player =1 - self.starting_player # takes 1->0 and 0->1
        self.lead_player = self.starting_player
        self.current_player = 1 - self.starting_player

        # deal hands 
        self.hands[0].add(self.deck.deal(10))
        self.hands[1].add(self.deck.deal(10))

        # deal piles

        self.piles.append(self.deck.deal(2))
        self.piles.append(self.deck.deal(2))
        
        
        self.phase = 'bid' #add the bid layer

    def legal_bets(self,player,last_bet=100):
        if self.phase != 'last_bet':
            bets = [0]
        else:
            bets = [last_bet]
        if last_bet>= self.hands[player].get_limit():
            return bets
        return bets + list(range(last_bet+10,self.hands[player].get_limit()+1,10))

    def bid(self,player,bet):

        if self.phase not in ['bid','last_bet'] :
            raise ValueError("Now is not the time to bet!")
        if player != self.current_player:
            raise ValueError("It is not your turn!")
        if bet not in self.legal_bets(player,max(self.bets)):
            raise ValueError("Not a legal bet!")
        
        if 0 == bet:
            self.bets[player]=0
            self.lead_player = 1- player
            self.current_player = self.lead_player
            self.phase = 'pile_selection'
        
        self.bets[player] = bet

        if self.phase != 'last_bet':
            self.current_player = 1 - player
        else:
            self.phase ='play'

    def choose_pile(self,pile):
        if self.phase != 'pile_selection':
            raise ValueError("Cannot choose a pile now!")
        chosen = self.piles[pile]
        print(f"Chosen pile is': {chosen}")
        self.piles[pile] = []
        self.discarded = self.piles[1-pile]
        print(self.discarded)
        self.hands[self.lead_player].add(chosen)
        self.phase = 'discard'

    def discard(self,cards):
        if self.phase != 'discard':
            raise ValueError("Cannot discard now!")    
        self.hands[self.lead_player].remove(cards)
        self.discarded.append(cards)
        if len(self.hands[self.lead_player])==10:
            self.phase = 'last_bet'

    def get_legal_moves(self, player):
        lead = self.table[0] if self.table else None
        return self.hands[player].legal_moves(self.trump_suit,lead)
    
    # Functions changing the state of the game

    def play_card(self, player ,card):

        if self.phase != 'play':
            raise ValueError("Now not the time to play a card!")
        if player != self.current_player:
            raise ValueError("It is not your turn!")
        
        if card not in self.get_legal_moves(player):
            raise ValueError("Cannot play this card!")
        
        # If you put down marriage it sets the trump suit
        if len(self.table)==0 and (card.suit in self.hands[player].marriages()) and card.rank in (Rank.KING,Rank.QUEEN):
            self.trump_suit = card.suit
            self.scores[player] += trump_points[card.suit]
        
        self.hands[player].remove(card)
        self.table.append(card)
    
        if len(self.table) == 1:
            self.current_player = 1 -player
        else:
            self._resolve_trick()


    
    def _resolve_trick(self):

        lead_card = self.table[0]
        follow_card =self.table[1]

        winner = self._trick_winner(lead_card,follow_card)
        points = lead_card.points + follow_card.points

        self.scores[winner] += points

        self.table =[]
        self.current_player = winner
        self.lead_player = winner

        if len(self.hands[0])==0:
            # add the points from the pile
            discarded_points = sum(c.points for c in self.discarded)
            self.scores[winner] += discarded_points
            # compare the scores to bets
            if self.scores[0]>= self.bets[0]:
                if self.bets[0] ==0:
                    self.game_points[0] += self.scores[0]
                else: 
                    self.game_points[0] += self.bets[0]
            else:
                self.game_points[0] -= self.bets[0]
            
            if self.scores[1]>= self.bets[1]:
                if self.bets[1] ==0:
                    self.game_points[1] += self.scores[1]
                else:
                    self.game_points[1] += self.bets[1]
            else:
                self.game_points[1] -= self.bets[1]

            self.phase = 'finished'
    

    def _trick_winner(self,lead,follow):
        lead_trump = lead.suit == self.trump_suit
        follow_trump = follow.suit == self.trump_suit

        if lead_trump and not follow_trump:
            return self.lead_player
        elif not lead_trump and follow_trump:
            return 1- self.lead_player 
        elif follow.suit != lead.suit:
            return self.lead_player
        elif follow.points > lead.points:
            return 1- self.lead_player 
        else:
            return self.lead_player
        
    def __repr__(self):
        return (f"Gamestate(phase = {self.phase}, trump={self.trump_suit}, "
                f"scores = {self.scores}, turn = P{self.current_player})"
                )




