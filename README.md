# Russian Schnapsen

A Python implementation of Russian Schnapsen (Polish variant), featuring a full
game engine, a pygame graphical interface, and (in progress) a reinforcement
learning agent trained through self-play.

## About the game

Russian Schnapsen is a trick-taking card game played with a 24-card deck
(9, J, Q, K, 10, A in each suit). This implementation follows the Polish
variant, which includes:

- **Bidding** — players bid on the score they believe they can achieve before
  the round starts
- **Pile selection** — players choose between two hidden piles of cards to
  add to their hand
- **Marriages** — playing a King or Queen of a suit where you hold both
  changes the trump suit and awards points based on suit
  (Spades: 40, Clubs: 60, Diamonds: 80, Hearts: 100)
- **Discard pile scoring** — the discarded cards are awarded to whoever wins
  the final trick of the round

## Features

- Full game engine enforcing all rules (trick-following, trump mechanics,
  marriages, bidding, pile selection, discarding, scoring)
- Playable via a pygame GUI with clickable cards, popups, and score tracking
- A random-move AI opponent for testing the game loop
- Planned: a reinforcement learning agent trained via self-play

## Project structure

```
russian-schnapsen/
├── cards.py         # Card, Suit, Rank classes
├── game_logic.py    # Gamestate — core rules engine
├── ai_logic.py       # AI helper functions (e.g. random_bet)
├── schnapsenGUI.py  # pygame GUI
├── cards/            # card image assets
└── README.md
```

## Requirements

- Python 3.10+
- pygame

## Installation

```bash
git clone https://github.com/miki-170/russian-schnapsen.git
cd russian-schnapsen
pip install pygame
```

## Running the game

```bash
python schnapsenGUI.py
```

## How to play

1. **Bidding phase** — click your bid amount, or "Pass"
2. **Pile selection** — click one of the two face-down piles to add its
   cards to your hand
3. **Discard phase** — click 2 cards to discard back down to a full hand
4. **Play phase** — click a card in your hand to play it; the game enforces
   legal moves (following suit, beating the lead card, trump rules)
5. Marriages are announced automatically when leading with a King or Queen
   of a suit where you hold the pair

## Roadmap

- [x] Core game engine (deck, hands, tricks, trump, marriages)
- [x] Bidding and pile selection mechanics
- [x] Pygame GUI with click-based interaction
- [ ] Rule-based baseline AI
- [ ] Reinforcement learning agent (DQN / PPO)
- [ ] Self-play training loop
- [ ] Evaluation against baseline and human play

## Learning journey

This project was built from scratch as a way to learn object-oriented Python
design, GUI development with pygame, and reinforcement learning fundamentals.
The AI component is currently in development, following a self-directed
study path through RL theory before implementation.

## License

MIT