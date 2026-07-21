import pygame
from game_logic import Gamestate
from cards import Suit, Rank
class GameGUI:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Russian Schnapsen')
        self.screen = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.state = Gamestate()
        self.state.start_new_round()
        self._load_images()
    

    # will fix it later
    def _load_images(self):
        self.card_boxes = {}
        for suit in Suit:
            for rank in Rank:
                filename = f"cards/Playing Cards/SVG-cards-1.3/"

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.start_new_round()
                
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
        self.draw_AI(0)

    def draw_hand(self):
        self.card_boxes = {}
        hand = self.state.hands[0]

        for i, card in enumerate(hand.cards):
            x = 65+ i * 90
            y = 550

            rect = pygame.Rect(x,y,70,100)
            pygame.draw.rect(self.screen,(255,255,255),rect)
            self.card_boxes[card] = rect

    def draw_AI(self,show:bool):
        self.card_boxes = {}
        hand = self.state.hands[1]
        if show == False:

            image = pygame.image.load("cards/card_back.png")
            image = pygame.transform.scale(image,(70,100))
            for i, card in enumerate(hand.cards):
                x = 65+ i * 90
                y = 50

                rect = pygame.Rect(x,y,70,100)
                self.screen.blit(image,(x,y))
                self.card_boxes[card] = rect

game = GameGUI()

game.run()

