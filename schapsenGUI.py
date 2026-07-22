import pygame
from game_logic import Gamestate
from cards import Suit, Rank
from random import choice
from ai_logic import random_bet
class GameGUI:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Russian Schnapsen')
        
        self.screen = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.state = Gamestate()
        self.player = True
        self.state.start_new_round()
        self.card_boxes = {}
        self.button_rects = {}
        
        self.x = self.screen.get_size()[0]
        self.y = self.screen.get_size()[1]

        self.card_x_size = 7/100*self.x
        self.card_y_size = 1/7*self.y

        self._load_images()
    
    def run(self):
        running = True
        self.error_message = None
        self.error_time = None

        while running:
            self.x = self.screen.get_size()[0]
            self.y = self.screen.get_size()[1]

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state.phase == 'bid':
                        self._handle_bet(event.pos)
                    try:
                        self.handle_click(event.pos)
                        
                    except Exception as e:
                        self.error_message = str(e)
                        self.error_time = pygame.time.get_ticks()

            if self.error_time and pygame.time.get_ticks() - self.error_time >2000:
                self.error_message = None
                self.error_time = None
                
            self.draw()

            # Section for betting 
            self.ai_bets()

            if self.error_message:
                self._draw_error(self.error_message)

            # renders the game
            pygame.display.flip()

            if self.player==False:
                pygame.time.delay(800)

            # limits fps to 60
            self.clock.tick(60)

        pygame.quit()



    def _load_images(self):
        names = { "9":"9","10":"10",'J':"jack",'Q':'queen','K':'king','A':'ace'}
        self.card_images = {}

        for suit in Suit:
            for rank in Rank:
                filename = f"cards/Playing Cards/PNG-cards-1.3/{names[rank.display]}_of_{str(suit.name).lower()}.png"
                
                try:
                    image = pygame.image.load(filename)
                    image = pygame.transform.scale(image,(self.y/10,self.x/10))
                    self.card_images[(suit,rank)] = image
                except:
                    raise FileNotFoundError("File path doesn't exist")

    def _draw_error(self, message):
    
        # white error text on top
        font = pygame.font.SysFont(None, 32)
        text = font.render(f"Error: {message}", True, (255, 255, 255))
        self.screen.blit(text, (self.x/5, self.y/2))

    def ai_bets(self):
        if self.state.current_player==1 and self.state.phase=='bid':
            self.state.bid(1,random_bet(self.state.legal_bets(1,max(self.state.bets))))
        if self.state.current_player==0 and self.state.phase=='bid' and self.player==False:
            self.state.bid(0,random_bet(self.state.legal_bets(0,max(self.state.bets))))
            

    def draw_pop_up(self):

        popup_x = self.x//3
        popup_y = self.y//3
        popup_width = int(self.x * 0.4)
        popup_height = int(self.y* 0.3)

        pop_up_rect = pygame.Rect(popup_x,popup_y,popup_width,popup_height)

        pygame.draw.rect(self.screen,(255,255,255),pop_up_rect)
        # black border
        pygame.draw.rect(self.screen, (0, 0, 0), pop_up_rect, 2)

        self.button_rects={}

        font_btn = pygame.font.SysFont(None, 32 * self.x//1000 )

        for j in range(3):
            button_width = popup_width//9
            button_height = popup_height//4
            for i in range(9):
                btn_x =  popup_x + button_width * i
                btn_y = popup_y + button_height * j

                if i == 8:
                    button_width = popup_x + popup_width - btn_x  
                
                points =100 + 90 * j + i * 10
                color = (128,128,128)

                btn_rect = pygame.Rect(btn_x,btn_y,button_width,button_height)
                pygame.draw.rect(self.screen, (0, 0, 0), btn_rect, 1)

                if points in self.state.legal_bets(0,max(self.state.bets)):
                    color = (0,0,0)
                    self.button_rects[points] = (btn_rect)

                text = font_btn.render(f"{points}",True,color)

                text_rect = text.get_rect(center=btn_rect.center)
                self.screen.blit(text, text_rect)
                
        
        text = font_btn.render("Pass",True,(0,0,0))
        pass_rect = pygame.Rect(popup_x, btn_y + button_height, popup_width,button_height )

        # position text rectangle with a centre in the bigger rectangle
        text_rect = text.get_rect(center= pass_rect.center)
        self.screen.blit(text, text_rect)

        self.button_rects[0] = pass_rect

    def draw(self):
        # fills the background with poker green
        self.screen.fill((53, 101, 77))
        if self.state.phase=='bid' and self.state.current_player==0 and self.player==True:
                self.draw_pop_up()
        self.draw_hand()
        self.draw_ai(not self.player)
        self.draw_piles()
        self.draw_scores()
        
    def handle_click(self, pos):
        self.error_message = None

        if self.state.phase=='play' and self.state.current_player==0:
            for card, rect in self.card_boxes.items():
                if rect.collidepoint(pos):
                    legal = self.state.get_legal_moves(0)
                    if card in legal:
                        self.state.play_card(0,card)
                        self.ai_move()
                    break
        
    def _handle_bet(self,pos):
        if self.state.phase == 'bid' and self.state.current_player==0:
            for bet, rect in self.button_rects.items():
                if rect.collidepoint(pos):
                    self.state.bid(0,bet)
                    if bet!= 0:
                        self.state.bid(1,random_bet(self.state.legal_bets(1,max(self.state.bets))))

    def ai_move(self):
        legal = self.state.get_legal_moves(1)
        card = choice(legal)
        self.state.play_card(1,card)

    def draw_piles(self):
        for i, pile in enumerate(self.state.piles):
            for j,card in enumerate(pile):
                x = (5+80*i)/100 *self.x + self.card_x_size/2*j
                y = self.y/3

                image = self.card_images[(card.suit, card.rank)]
                image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))
                self.screen.blit(image,(x,y))

    def draw_hand(self):
        
        self.card_boxes = {}

        hand = self.state.hands[0]

        for i, card in enumerate(hand.cards):
            x = 0.065* self.x+ i * 0.09 * self.x
            y = 550/700 * self.y
            
            image = self.card_images[(card.suit, card.rank)]
            image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))
            self.screen.blit(image,(x,y))
            
            if self.state.phase == 'play':
                self.card_boxes[card] = pygame.Rect(x,y,self.card_x_size,self.card_y_size)

    def draw_ai(self,show:bool):
        
        hand = self.state.hands[1]

        # also add an option to draw all the cards

        for i, card in enumerate(hand.cards):
            if show == False:
                image = pygame.image.load("cards/card_back.png")
                image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))
            else:
                image = self.card_images[(card.suit, card.rank)]
                image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))

            x = 0.065 * self.x + i * 0.09 * self.x
            y = 50/700 * self.y
            self.screen.blit(image,(x,y))
            self.card_boxes[card] = pygame.Rect(x,y,self.card_x_size,self.card_y_size)
                
    def draw_scores(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Turn: {self.state.current_player}; You: {self.state.scores[0]}, Bet: {self.state.bets[0]}  AI: {self.state.scores[1]}, Bet: {self.state.bets[1]}",True,(255,255,255))
        self.screen.blit(text,(20,20))

game = GameGUI()
#game.player = False
game.run()

