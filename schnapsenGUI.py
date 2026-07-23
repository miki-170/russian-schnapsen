import pygame
from game_logic import Gamestate
from cards import Suit, Rank
from ai_logic import ai_random

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
        self.pile_rects= {}
        
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
                    
                    if self.state.phase== 'bid' or self.state.phase== 'last_bet':
                        self.handle_bet(event.pos)
                    elif self.state.phase == 'pile_selection':
                        self.chosing_pile(event.pos)
                    elif self.state.phase == 'discard':
                        self.handle_discard(event.pos)

                    else:
                        self.handle_click(event.pos)
                        
            
            
            self.draw()

            if self.state.phase == 'finished':
                self.state.start_new_round()

            if self.state.phase == 'play':
                ai_random.ai_move(0,self)

            if self.state.phase == 'discard':
                ai_random.ai_discard(0,self)

            # Section for betting 
            if self.state.phase=='bid' or self.state.phase=='last_bet':
                ai_random.ai_bets(0,self)

            if self.state.phase == 'pile_selection':
                ai_random.ai_pile_select(0,self)

            # renders the game
            pygame.display.flip()

            if self.player==False:
                pygame.time.delay(1000)

            # limits fps to 60
            self.clock.tick(60)

        pygame.quit()

    def _load_images(self):
        names = { "9":"9","10":"10",'J':"jack",'Q':'queen','K':'king','A':'ace'}
        self.card_images = {}

        self.card_back = pygame.image.load("cards/card_back.png")
        self.card_back = pygame.transform.scale(self.card_back,(self.card_x_size,self.card_y_size))

        for suit in Suit:
            for rank in Rank:
                filename = f"cards/Playing Cards/PNG-cards-1.3/{names[rank.display]}_of_{str(suit.name).lower()}.png"
                
                try:
                    image = pygame.image.load(filename)
                    image = pygame.transform.scale(image,(self.y/10,self.x/10))
                    self.card_images[(suit,rank)] = image
                except:
                    raise FileNotFoundError("File path doesn't exist")

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
                
        if self.state.phase =='bid':   
            color = (0,0,0)
        else:
            color =(128,128,128)
        text = font_btn.render("Pass",True,color)
        pass_rect = pygame.Rect(popup_x, btn_y + button_height, popup_width,button_height )

        # position text rectangle with a centre in the bigger rectangle
        text_rect = text.get_rect(center= pass_rect.center)
        self.screen.blit(text, text_rect)  

        if self.state.phase =='bid':   
            self.button_rects[0] = pass_rect

    def draw(self):
        # fills the background with poker green
        self.screen.fill((53, 101, 77))
        if (self.state.phase=='bid' or self.state.phase=='last_bet') and self.state.current_player==0 and self.player==True:
                self.draw_pop_up()
        self.draw_hand()
        self.draw_ai(not self.player)
        self.draw_piles()
        self.draw_scores()
        self.draw_table()
        
    def handle_click(self, pos):
        self.error_message = None

        if self.state.phase=='play' and self.state.current_player==0:
            for card, rect in self.card_boxes.items():
                if rect.collidepoint(pos):
                    legal = self.state.get_legal_moves(0)
                    if card in legal:
                        self.state.play_card(0,card)
                    break
        
    def handle_bet(self,pos):
        if (self.state.phase == 'bid' or self.state.phase == 'last_bet') and self.state.current_player==0:
            for bet, rect in self.button_rects.items():
                if rect.collidepoint(pos):
                    self.state.bid(0,bet)

    def handle_discard(self,pos):
        if self.state.phase == 'discard' and self.state.current_player==0:
            for card, rect in self.card_boxes.items():
                if rect.collidepoint(pos):
                    self.state.discard(card)

    def draw_piles(self):
        self.pile_rects= {}
        for i, pile in enumerate(self.state.piles):
            pile_rect = None
            for j,card in enumerate(pile):
                x = (5+80*i)/100 *self.x + self.card_x_size/2*j
                y = self.y/3
                
                if i == self.state.chosen_pile :
                    if j<2:
                        image = self.card_images[(card.suit, card.rank)]
                        image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))
                        self.screen.blit(image,(x,y))
                
                else:
                    
                    image = self.card_back
                    self.screen.blit(image,(x,y))

                    if self.state.phase == 'pile_selection':
                        card_rect = pygame.Rect(x, y, self.card_x_size, self.card_y_size)
                        if pile_rect is None:
                            pile_rect = card_rect
                        else:
                            pile_rect = pile_rect.union(card_rect)
                        self.pile_rects[i] = pile_rect
                
    def chosing_pile(self,pos):
        if self.state.phase == 'pile_selection' and self.state.current_player==0:
            for pile, rect in self.pile_rects.items():
                if rect.collidepoint(pos):
                    self.state.chosen_pile = pile
                    self.state.choose_pile(pile)

    def draw_hand(self):
        
        self.card_boxes = {}

        hand = self.state.hands[0]

        count = len(hand)
        
        for i, card in enumerate(hand.cards):
            x = 0.005* self.x * (i+1) + i * self.card_x_size
            y = 550/700 * self.y
            
            image = self.card_images[(card.suit, card.rank)]
            image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))
            self.screen.blit(image,(x,y))
            
            if self.state.phase == 'play' or (self.state.phase == 'discard' and self.state.current_player==0):
                self.card_boxes[card] = pygame.Rect(x,y,self.card_x_size,self.card_y_size)

    def draw_ai(self,show:bool):
        
        hand = self.state.hands[1]

        for i, card in enumerate(hand.cards):
            if show == False:
                image = self.card_back
            else:
                image = self.card_images[(card.suit, card.rank)]
                image = pygame.transform.scale(image,(self.card_x_size,self.card_y_size))

            x = 0.005* self.x * (i+1) + i * self.card_x_size
            y = 50/700 * self.y
            self.screen.blit(image,(x,y))
            #self.card_boxes[card] = pygame.Rect(x,y,self.card_x_size,self.card_y_size)

    def draw_table(self):
        table = self.state.table

        if len(table)==0:
            return 
        
        center_x = self.x // 2
        center_y = self.y // 2
        gap = 10

        total_width = self.card_x_size * 2 + gap
        x = center_x - total_width // 2
        y = center_y - self.card_y_size // 2

        for i, cards in enumerate(table):
            self.screen.blit(self.card_images[(cards.suit, cards.rank)], (x + i * (self.card_x_size + gap),y))

    def draw_scores(self):
        leader = self.state.bets.index(max(self.state.bets))
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Turn: {self.state.current_player}; Phase: {self.state.phase}; Total score: {self.state.game_points[0]} : {self.state.game_points[1]}",True,(255,255,255))
        self.screen.blit(text,(20,5))
        text = font.render(f"You: {self.state.scores[0]},  AI: {self.state.scores[1]}, Bet: {max(self.state.bets)} on {leader}. Trump: {self.state.trump_suit} ",True,(255,255,255))
        self.screen.blit(text,(20,30))

game = GameGUI()
#game.player = False
game.run()

