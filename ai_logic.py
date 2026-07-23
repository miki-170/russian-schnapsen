from random import choice

class ai_random:
    def __init__(self):
        pass

    def ai_bets(self,x):
        if x.state.current_player==1:
            x.state.bid(1,choice(x.state.legal_bets(1,max(x.state.bets))))
        elif x.state.current_player==0 and (x.state.phase=='bid' or x.state.phase == 'last_bet') and x.player==False:
            x.state.bid(0,choice(x.state.legal_bets(0,max(x.state.bets))))

    def ai_move(self,x):
        if x.state.current_player==1:
            legal = x.state.get_legal_moves(1)
            card = choice(legal)
            x.state.play_card(1,card)
        
        elif x.state.current_player==0 and x.state.phase=='play' and x.player==False:
            
            legal = x.state.get_legal_moves(0)
            card = choice(legal)
            x.state.play_card(0,card)

    def ai_discard(self,x):
        if x.state.current_player==1:
            card = choice(x.state.hands[1].cards)
            x.state.discard(card)

        elif x.state.current_player==0 and x.state.phase=='discard' and x.player==False:
            card = choice(x.state.hands[0].cards)
            x.state.discard(card)

    def ai_pile_select(self,x):
        if x.state.current_player==1:
            pile = choice([0,1])
            x.state.chosen_pile = pile
            x.state.choose_pile(pile)
        
        elif x.state.current_player==0 and x.state.phase=='pile_selection' and x.player==False:
            pile = choice([0,1])
            x.state.chosen_pile = pile
            x.state.choose_pile(pile)
