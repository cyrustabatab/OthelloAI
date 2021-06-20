import pygame,sys
pygame.init()




SCREEN_HEIGHT = SCREEN_WIDTH =  800



BGCOLOR = (231,255,208)
GREEN = (0,190,0)
WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)




class Button(pygame.sprite.Sprite):


    def __init__(self,x,y,button_width,button_height,text,text_color,button_color,font):
        super().__init__()


        self.original_image = pygame.Surface((button_width,button_height))
        self.expanded_image = pygame.Surface((button_width + 20,button_height + 20))
        self.original_rect = self.original_image.get_rect(topleft=(x,y))
        self.expanded_rect = self.expanded_image.get_rect(center=self.original_rect.center)


        self.images = [(self.original_image,self.original_rect),(self.expanded_image,self.expanded_rect)]
        text = font.render(text,True,text_color)

        for image,_ in self.images:
            image.fill(button_color)
            image.blit(text,(image.get_width()//2 - text.get_width()//2,image.get_height()//2 - text.get_height()//2))

        self.image_index = 0
        self.image,self.rect = self.images[self.image_index]

        self.hovered_on = False

    def update(self,point):

        collided = self.rect.collidepoint(point)

        if (self.hovered_on and not collided) or (not self.hovered_on and collided):
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image,self.rect = self.images[self.image_index]
            self.hovered_on = not self.hovered_on


    

    def collided_on(self,point):


        return self.rect.collidepoint(point)

class Game:

    TOP_GAP = 100
    RIGHT_GAP = 250
    def __init__(self,screen,rows=8,cols=8,ai=False):
        



        self.rows = rows
        self.cols = cols
        
        self.square_size = (screen.get_height() - self.TOP_GAP)//self.rows
        self.screen_height = self.square_size * rows + self.TOP_GAP
        self.screen_width = self.square_size * cols + self.RIGHT_GAP
        self.board_width = self.square_size * cols
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.ai = ai
        self.board_surface = pygame.Surface((rows * self.square_size,cols * self.square_size))
        self.board_surface.fill(GREEN)
        self._initialize_board()
        self.play()


    def _initialize_board(self):


        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]



    def play(self):


        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.screen.fill(BGCOLOR) 
            self.screen.blit(self.board_surface,(0,self.TOP_GAP))
            self.draw_board()
            pygame.display.update()


    def draw_board(self):


        for row in range(self.TOP_GAP,self.screen_height,self.square_size):
            pygame.draw.line(self.screen,BLACK,(0,row),(self.board_width,row))


        for col in range(0,self.board_width + 1,self.square_size):
            pygame.draw.line(self.screen,BLACK,(col,self.TOP_GAP),(col,self.screen_height))







class Menu:
    
    
    title_font = pygame.font.SysFont("calibri",100)


    def __init__(self,screen_width=800,screen_height=800):
        

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        button_width = 200 
        button_height = 100
        start_button = Button(self.screen_width//2 - button_width//2,self.screen_height//2 - button_height//2,button_width,button_height,"PLAY",BLACK,RED,self.title_font)

        self.buttons = pygame.sprite.Group(start_button)
        self.title_text = self.title_font.render("OTHELLO",True,BLACK)

        pygame.display.set_caption("OTHELLO")
        self.start()

    

    def get_board_size(self):

        



        text = self.title_font.render("BOARD SIZE",True,BLACK)
        top_gap = 50
        text_rect = text.get_rect(center=(self.screen_width//2,top_gap + text.get_height()//2))

        FLICKERING_EVENT = pygame.USEREVENT + 2

        
        user_answer = '|'

        user_text = self.title_font.render(user_answer,True,BLACK)
        width = user_text.get_width()


        pygame.time.set_timer(FLICKERING_EVENT,200)

        
        def get_true_width():

            if user_answer and user_answer[-1] == '|':
                width= self.title_font.render(user_answer[:-1],True,BLACK).get_width()
            else:
                width= self.title_font.render(user_answer,True,BLACK).get_width()

            return width

        backspace_pressed = False
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.K_0 <= event.key <= pygame.K_9:


                        if user_answer and user_answer[-1] == '|':
                            
                            user_answer = user_answer[:-1] + chr(event.key) + '|'
                        else:
                            user_answer += chr(event.key)


                        user_text = self.title_font.render(user_answer,True,BLACK)
                        width = get_true_width()
                    elif event.key == pygame.K_RETURN:
                        if user_answer:
                            user_answer = user_answer[:-1] if user_answer[-1] == '|' else user_answer

                            return int(user_answer)
                    elif event.key == pygame.K_BACKSPACE:
                        if user_answer:
                            last = user_answer[-1]
                            if last == '|':
                                user_answer = user_answer[:-2]
                            else:
                                user_answer = user_answer[:-1]

                            user_text = self.title_font.render(user_answer,True,BLACK)
                            width = get_true_width()



                if event.type == FLICKERING_EVENT:

                    if user_answer and user_answer[-1] == '|':
                        user_answer = user_answer[:-1]
                    else:
                        user_answer = user_answer + '|'

                    user_text = self.title_font.render(user_answer,True,BLACK)
                    width = get_true_width()
            




            self.screen.fill(GREEN)
            self.screen.blit(text,text_rect)

             
            self.screen.blit(user_text,(self.screen_width//2 - width//2,self.screen_height//2 - user_text.get_height()//2))
            pygame.display.update()




    
    def ai_or_regular_screen(self):

        
        button_width,button_height = 550,120

        gap_between_buttons = 100
        

        top_and_bottom_gap = (self.screen_height- button_height * 2 - gap_between_buttons)//2

        
        buttons = pygame.sprite.Group()
        buttons_list = []
        texts = ['TWO PLAYER','COMPUTER']
        for i in range(2):
            button = Button(self.screen_width//2 - button_width//2,top_and_bottom_gap + (button_height + gap_between_buttons) * i,button_width,button_height,texts[i],BLACK,RED,self.title_font)
            buttons.add(button)
            buttons_list.append(button)



        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()


                    if buttons_list[0].collided_on(point):
                        return



            point = pygame.mouse.get_pos() 

            buttons.update(point)
            
            self.screen.fill(GREEN)
            buttons.draw(self.screen)
            pygame.display.update()

    def start(self):


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Game(self.screen)
                        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()


                    for i,button in enumerate(self.buttons):
                        collided = button.collided_on(point)
                        if collided:
                            self.ai_or_regular_screen()
                            size = self.get_board_size()
                            pygame.display.set_caption(f"OTHELLO {size} x {size}")
                            Game(self.screen,size,size)




                    

                    

            
            point = pygame.mouse.get_pos()
            self.buttons.update(point)


            self.screen.fill(GREEN)
            self.screen.blit(self.title_text,(self.screen_width//2 - self.title_text.get_width()//2,50))
            self.buttons.draw(self.screen)
            pygame.display.update()










if __name__ == "__main__":
    
    Menu()






