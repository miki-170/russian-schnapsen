import pygame
from game_logic import Gamestate
from cards import Suit, Rank
from random import choice
class GameGUI:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Russian Schnapsen')
        self.screen = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.state = Gamestate()
        self.state.start_new_round()
        self._load_images()
        self.card_boxes = {}
        

    # will fix it later
    def _load_images(self):
        names = { "9":"9","10":"10",'J':"jack",'Q':'queen','K':'king','A':'ace'}
        self.card_images = {}
        for suit in Suit:
            for rank in Rank:
                filename = f"cards/Playing Cards/PNG-cards-1.3/{names[rank.display]}_of_{str(suit.name).lower()}.png"
                
                try:
                    image = pygame.image.load(filename)
                    image = pygame.transform.scale(image,(70,100))
                    self.card_images[(suit,rank)] = image
                except:
                    raise FileNotFoundError("File path doesn't exist")

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
            self.draw()

            # renders the game
            pygame.display.flip()

            # limits fps to 60
            self.clock.tick(60)

        pygame.quit()

    def draw(self):
        # fills the background with poker green
        self.screen.fill((53, 101, 77))
        self.draw_hand()
        self.draw_ai(0)
        self.draw_scores()

    def handle_click(self, pos):
        for card, rect in self.card_boxes.items():
            if rect.collidepoint(pos):
                legal = self.state.get_legal_moves(0)
                print(card)
                if card in legal:
                    self.state.play_card(0,card)
                    self.ai_move()
                break
    
    def ai_move(self):
        legal = self.state.get_legal_moves(1)
        card = choice(legal)
        self.state.play_card(1,card)

    def draw_hand(self):
        
        hand = self.state.hands[0]

        for i, card in enumerate(hand.cards):
            x = 65+ i * 90
            y = 550
            
            image = self.card_images[(card.suit, card.rank)]
            self.screen.blit(image,(x,y))
            
            self.card_boxes[card] = pygame.Rect(x,y,70,100)

    def draw_ai(self,show:bool):
        
        hand = self.state.hands[1]

        # also add an option to draw all the cards
        if show == False:

            image = pygame.image.load("cards/card_back.png")
            image = pygame.transform.scale(image,(70,100))
            for i, card in enumerate(hand.cards):
                x = 65+ i * 90
                y = 50
                self.screen.blit(image,(x,y))
        else:
            hand = self.state.hands[1]

            for i, card in enumerate(hand.cards):
                x = 65+ i * 90
                y = 550
                
                image = self.card_images[(card.suit, card.rank)]
                self.screen.blit(image,(x,y))
                self.card_boxes[card] = pygame.Rect(x,y,70,100)
                
    def draw_scores(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Turn: {self.state.current_player}; You: {self.state.scores[0]}  AI: {self.state.scores[1]}",True,(255,255,255))
        self.screen.blit(text,(20,20))

game = GameGUI()

game.run()

