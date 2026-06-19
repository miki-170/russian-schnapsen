from game_logic import Gamestate
import random

def display_state(state):
    print("\n" + "-" * 40 )
    print(f"Trump suit: {state.trump_suit}.")
    print(f"Your hand: {state.hands[0]}.")
    print(f"AI hand: {state.hands[1]}.")
    print(f"Score — You: {state.scores[0]}  AI: {state.scores[1]}")
    print(f"Bets - You: {state.bets[0]} AI: {state.bets[1]} ")
    print(f"Points - You: {state.game_points[0]} AI: {state.game_points[1]}")
    if state.table:
        print(f"Table: {state.table}")
    print("-"*40)
    

def get_human_bid(state):
    legal = state.legal_bets(0,max(state.bets))

    print("\n Your legal bets")
    for i, n in enumerate(legal):
        print(f"{i}. - {n}")

    while True:
        try:
            choice = int(input("Choose your bet:"))
            if 0<=choice <len(legal):
                return legal[choice]
            else:
                print("Invalid number, try again.")
        except ValueError: 
            print("Choose a number!")


def get_human_move(state):
    legal = state.get_legal_moves(0)
    if state.phase =='discard':
        print("\n Discard a card:")
    else:
        print("\n Your legal moves:")
    for i, card in enumerate(legal):
        print(f"{i}. - {card}")

    while True:
        try:
            choice =int( input("Choose a card:"))
            if 0<= choice < len(legal):
                return legal[choice]
            else:
                print("Invalid number, try again!")

        except ValueError: 
            print("Choose a number!")

def AI_discard_at_random(state):
    for _ in range(2):
        card = random.choice(state.hands[1].cards)
        state.discard(card)
    



def main():
    state = Gamestate()
    print("Start!")
    
    while max(state.game_points)<1000:
        
        state.start_new_round()



        while state.phase == 'bid':
            if state.current_player == 0:
                print(f"Your hand: {state.hands[0]}.")
                bet0 = get_human_bid(state)
                state.bid(0,bet0)
                print(f"Your bet is: {bet0}")
                continue
            if state.current_player ==1:
                legal = state.legal_bets(1,max(state.bets))
                bet1 =random.choice(legal)
                state.bid(1,bet1)
                print(f"AI's bet is: {bet1}")
                continue

        state.choose_pile(random.choice([0,1]))

        if state.current_player ==1 :
            AI_discard_at_random(state)
            legal = state.legal_bets(1,max(state.bets))
            bet1 =random.choice(legal)
            state.bid(1,bet1)
            print(f"AI is playing: {bet1}")
        else:
            for _ in range(2):
                discard = (get_human_move(state))
                state.discard(discard)
            print(f"Your hand: {state.hands[0]}.")
            bet0 = get_human_bid(state)
            state.bid(0,bet0)
            print(f"You are playing: {bet0}")

        while state.phase != 'finished':
            display_state(state)

            if state.current_player ==0:
                card = get_human_move(state)
                
                if len(state.table) ==1:
                    print(f"\n You responded with {card}.")
                else:
                    print(f"\n You started with {card}.")
                
                state.play_card(0,card)

            else:
                legal = state.get_legal_moves(1)
                card = random.choice(legal)
                
                if len(state.table) ==1:
                    print(f"\n AI responded with {card}.")
                else:
                    print(f"\n AI started with {card}.")

                state.play_card(1,card)

        print("Game Over!")
        display_state(state)

    if state.game_points[0] > state.game_points[1]:
        print(f"Player 0 won!")
    else:
        print(f"Player 1 won!")
    
    

if __name__ == "__main__":
    main()