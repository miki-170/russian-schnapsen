import pygame
from game_logic import Gamestate
class GameGUI:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Russian Schnapsen')
        self.screen = pygame.display.set_mode((600,600), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.state = Gamestate()
        self.state.start_new_round()
        self.card_boxes = {}
    
    def run(self):
        running = True

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

game = GameGUI()

game.run()

