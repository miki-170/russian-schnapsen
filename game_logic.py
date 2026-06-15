from cards import Card,Deck,Hand


class Gamestate:
    
    def __init__(self):
        self.deck = Deck()  # initialising deck
        self.hands = [Hand(),Hand()]    #players' hands
        self.piles = [Hand(),Hand()]    # initial piles
        self.trump_suit = None  # current trump suit
        self.lead_player = 0    # who starts the round
        self.current_player = 0 
        self.played_card = None
        self.table = []
        self.scores = [0,0] # score in this trick
        self.game_points= [0,0]     # total scores 
        self.current_player = 0     # 
        self.phase = 'deal'     # deal -> bid -> play -> finished
        self.anounced_marriages = []    

    def start_new_round(self):
        self.deck = Deck()
        # shuffle the deck
        self.deck.shuffle()

        # reset all
        self.hands = [Hand(),Hand()]   
        self.piles = [Hand(),Hand()]  
        self.trump_suit = None
        self.played_card = None
        self.scores = [0,0]
        self.anounced_marriages = [] 
        self.phase = 'deal'
        self.lead_player =1 - self.lead_player # takes 1->0 and 0->1
        self.current_player = self.lead_player

        # deal hands 
        self.hands[0].add(self.deck.deal(10))
        self.hands[1].add(self.deck.deal(10))

        # deal piles

        self.piles[0].add(self.deck.deal(2))
        self.piles[1].add(self.deck.deal(2))
        
        # set player 0 as a starting one
        self.current_player = 0
        self.phase = 'play' #add the bid layer

    def get_legal_moves(self, player):
        return self.hands[player].legal_moves(self.trump_suit,self.played_card)
    
    # Functions changing the state of the game

    def play_card(self, player ,card):
        if player != self.current_player:
            raise ValueError("It is not your turn!")
        
        if card not in self.get_legal_moves(player):
            raise ValueError("Cannot play this card!")
        
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

        if len(self.hands[0])==0:
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





