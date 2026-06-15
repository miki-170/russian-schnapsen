from cards import Deck, Hand, Card
from game_logic import Gamestate
import random

def display_state(state):
    print("\n" + "-" * 40 )
    print(f"Trump suit: {state.trump_suit}.")
    print(f"Your hand: {state.hands[0]}.")
    print(f"AI hand: {state.hands[1]}.")
    print(f"Score — You: {state.scores[0]}  AI: {state.scores[1]}")
    if state.table:
        print(f"Table: {state.table}")
    print("-"*40)
    

def get_human_move(state):
    legal = state.get_legal_moves(0)

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


def main():
    state = Gamestate()
    state.start_new_round()

    print("Start!")

    while state.phase != 'finished':
        display_state(state)

        if state.current_player ==0:
            card = get_human_move(state)
            state.play_card(0,card)
            print(f"\n You played {card}. This card is {len(state.table)}")

        else:
            legal = state.get_legal_moves(1)
            card = random.choice(legal)
            state.play_card(1,card)
            print(f"\n AI played: {card}. This card is {len(state.table)}")
    
    print("Game Over!")
    print(display_state(state))


if __name__ == "__main__":
    main()