import pygame,sys,time,random
pygame.init()




SCREEN_HEIGHT = SCREEN_WIDTH =  800



BGCOLOR = (231,255,208)
BGCOLOR = (222,184,135)
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
    font = pygame.font.SysFont("calibri",50,bold=True)
    score_font = pygame.font.SysFont("calibri",40,bold=True)
    music = "music.ogg"
    invalid_move_effect = pygame.mixer.Sound("wrong.wav")
    place_effect = pygame.mixer.Sound("pop_sound.wav")
    win_sound = pygame.mixer.Sound("win.wav")
    tie_sound = pygame.mixer.Sound("tie.wav")

    def __init__(self,screen,rows=8,cols=8,ai=False):



        self.rows = rows
        self.cols = cols
        

        self.square_size = (screen.get_height() - self.TOP_GAP)//self.rows
        self.screen_height = self.square_size * rows + self.TOP_GAP
        self.screen_width = self.square_size * cols + self.RIGHT_GAP
        self.board_width = self.square_size * cols
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.circle_gap = self.square_size//2 - 10

        self.ai = ai
        self.board_surface = pygame.Surface((rows * self.square_size,cols * self.square_size))
        self.surface = pygame.Surface((self.square_size,self.square_size),pygame.SRCALPHA)
        self.board_surface.fill(GREEN)
        self._initialize_board()


        self.ai = ai
        self.turn = 'W'
        if ai:
            self.computer_piece = random.choice(['W','B'])
            self.user_piece = 'W' if self.computer_piece == 'B' else 'B'
        self.black_score = self.white_score = 2
        self.game_over = False

        self.black_score_text = self.score_font.render(f"{2:<3}",True,BLACK)
        self.white_score_text = self.score_font.render(f"{2:<3}",True,WHITE)
        self.transparent_color = (255,255,255,128)
        if not ai:
            self.mapping = {'W': ('WHITE',WHITE),'B': ("BLACK",BLACK)}
        else:
            computer_color,user_color = (WHITE,BLACK) if self.computer_piece == 'W' else (BLACK,WHITE)
            self.mapping = {self.computer_piece: ('AI',computer_color),self.user_piece: ('PLAYER',user_color)}





        self.turn_text = self.font.render(self.mapping[self.turn][0]+'\'S TURN',True,self.mapping[self.turn][1])
        self.invalid_text = self.font.render("INVALID MOVE!",True,RED)
        self._find_valid_moves()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
        self.play()
    



    def _initialize_board(self):


        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        self.board[self.rows//2 - 1][self.cols//2 - 1] = 'W'
        self.board[self.rows//2 - 1][self.cols//2] = 'B'
        self.board[self.rows//2][self.cols//2 - 1] = 'B'
        self.board[self.rows//2][self.cols//2] = 'W'

    

    def _switch_turns(self):

        if self.turn == 'W':
            self.turn = 'B'
            self.transparent_color = (0,0,0,128)
        else:
            self.turn = 'W'
            self.transparent_color = (255,255,255,128)
        

        self.turn_text = self.font.render(self.mapping[self.turn][0] + 'S TURN',True,self.mapping[self.turn][1])
    

    def _check_validity(self,row,col,checking=False):


        opposite_piece = 'W' if self.turn == 'B' else 'B'

        valid_move = False

        
        if checking:
            valid_squares = set()

        for i in (-1,0,1):
            for j in (-1,0,1):
                if i == 0 and j == 0:
                    continue
                

                valid =  self._check(board,row,col,i,j,opposite_piece,checking)
                if checking and valid:
                    return True
                valid_move = valid or valid_move


        return valid_move


    
    def _switch_color(self,row,col):
        


        if self.board[row][col] == 'W':
            self.board[row][col] = 'B'
            self.white_score -= 1
            self.black_score += 1
        else:
            self.board[row][col] = 'W'
            self.white_score += 1
            self.black_score -= 1






    
    def _check(self,row,col,row_diff,col_diff,opposite_piece,checking):

        
        
        in_bounds = lambda row,col: 0 <= row < self.rows and 0 <= col < self.cols
        

        current_row = row + row_diff
        current_col = col + col_diff



        while in_bounds(current_row,current_col) and self.board[current_row][current_col] == opposite_piece:
            current_row += row_diff
            current_col += col_diff
        
        

        if in_bounds(current_row,current_col) and self.board[current_row][current_col] == self.turn and abs(current_row - row) != 1 and abs(current_col - col) != 1:

            
            if not checking:
                current_row -= row_diff
                current_col -= col_diff

                while current_row != row or current_col != col:
                    self._switch_color(current_row,current_col)
                    current_row -= row_diff
                    current_col -= col_diff
            return True

        else:
            return False

    
    



    
    def _is_terminal_state(board):


        return not self._get_moves(board)



    def _get_moves(self,board):
        pass







        


    

    def _heuristic(self):
        pass






    
    def _ai_make_move(self):
        # for now make a random move but obviously make smarter ai in the end
        
        self.previous_white_score,self.previous_black_score = j

        return self._make_random_move()
    


    def _minimax(self,board,depth=5,ai=True):

        if self._is_terminal_state(board) or depth == 0:
            return self._heuristic(board)



        if ai:
            best_score = float("-inf")
            comparator = lambda x,y: x > y
        else:
            comparator = lambda x,y: x < y
            best_score = float("inf")
        best_move = None
        
        for move in self._get_moves(board):
            new_board = self._make_move(board)
            score,_ = self._minimax(new_board,depth -1,not ai)
            if comparator(score,maximum):
                best_score = score
                best_move = move
        

        return best_score,best_move




                








    def _make_random_move(self):

        
        moves = list(self.valid_moves)
        return random.choice(moves)
    
    def _find_valid_moves(self,checking=False):

        
        self.valid_moves = set()


        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    if self._check_validity(board,row,col,checking=True):
                        if checking:
                            return False
                        self.valid_moves.add((row,col))

    


    def _draw_score(self):


        radius = 30
        pygame.draw.circle(self.screen,BLACK,(self.screen_width - self.black_score_text.get_width() - radius,radius + 5),radius)
        pygame.draw.circle(self.screen,WHITE,(self.screen_width - self.black_score_text.get_width() - radius,3 * radius +5+ radius//2  ),radius)


        self.screen.blit(self.black_score_text,(self.screen_width - 2 * self.black_score_text.get_width() - 2 * radius,5 + radius//2 ))
        self.screen.blit(self.white_score_text,(self.screen_width - 2 * self.white_score_text.get_width() - 2 * radius,5 + 2 * radius + radius//2 ))

    
    
    def _reset(self):


        self.turn = 'W'
        self.turn_text = self.font.render(self.mapping[self.turn][0] + 'S TURN',True,self.mapping[self.turn][1])
        self.white_score = self.black_score = 2
        self.white_score_text = self.score_font.render(f"{2:<3}",True,WHITE)
        self.black_score_text = self.score_font.render(f"{2:<3}",True,BLACK)
        self._initialize_board()
        self.game_over= False
        self._find_valid_moves()




    def play(self):

        
        
        button_width = 200
        button_height = 100
        font = pygame.font.SysFont("calibri",30)
        play_again_button = Button(self.screen_width - (self.screen_width - self.board_width)//2 - button_width//2,self.screen_height//2 - button_height//2,button_width,button_height,"PLAY AGAIN",WHITE,BLACK,font)
        gap = 50
        menu_button = Button(self.screen_width - (self.screen_width - self.board_width)//2 - button_width//2,self.screen_height//2+ button_height//2 + gap + button_height//2,button_width,button_height,"MENU",WHITE,BLACK,font)


        game_buttons = pygame.sprite.Group(play_again_button,menu_button)


        invalid_move = game_over = False
        
        ai_start = None
        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    point = pygame.mouse.get_pos()
                    x,y = point

                    if not self.game_over and (not self.ai or (self.ai and self.user_piece == self.turn)):
                        if y > self.TOP_GAP and x < self.board_width:
                            row,col = (y - self.TOP_GAP)//self.square_size,x//self.square_size 
                            if (row,col) in self.valid_moves:
                                self._check_validity(row,col)
                                self.place_effect.play() 
                                self.board[row][col] = self.turn
                                if self.turn == 'W':
                                    self.white_score += 1
                                else:
                                    self.black_score += 1
                                
                                self.white_score_text = self.score_font.render(f"{self.white_score:<3}",True,BLACK)
                                self.black_score_text = self.score_font.render(f"{self.black_score:<3}",True,BLACK)

                                self._switch_turns()
                                self._find_valid_moves()
                                if not self.valid_moves:
                                    winner = 'BLACK WINS!' if self.black_score > self.white_score else 'WHITE WINS!' if self.white_score > self.black_score else 'TIE'

                                    if winner == 'TIE':
                                        self.tie_sound.play()
                                    else:
                                        self.win_sound.play()
                                    winner_text= self.font.render(winner,True,BLACK if winner[0] == 'B' else WHITE)


                                    self.game_over= True
                                invalid_move = False
                            else:
                                self.invalid_move_effect.play()
                                invalid_move = True
                                invalid_start = time.time()
                    else:

                        for i,button in enumerate(game_buttons):
                            if button.collided_on(point):
                                if i == 0:
                                    self._reset()
                                else:
                                    return
            


            if not self.game_over and self.ai and self.turn == self.computer_piece:
                if not ai_start:
                    ai_start= time.time()
                else:
                    current_time = time.time()
                    if current_time - ai_start >= 1:
                        row,col = self._ai_make_move()
                        self._check_validity(row,col)
                        self.place_effect.play() 
                        self.board[row][col] = self.turn
                        ai_start = None
                        if self.turn == 'W':
                            self.white_score += 1
                        else:
                            self.black_score += 1
                        
                        self.white_score_text = self.score_font.render(f"{self.white_score:<3}",True,BLACK)
                        self.black_score_text = self.score_font.render(f"{self.black_score:<3}",True,BLACK)

                        self._switch_turns()
                        self._find_valid_moves()
                        if not self.valid_moves:
                            winner = 'BLACK WINS!' if self.black_score > self.white_score else 'WHITE WINS!' if self.white_score > self.black_score else 'TIE'

                            if winner == 'TIE':
                                self.tie_sound.play()
                            else:
                                self.win_sound.play()
                            winner_text= self.font.render(winner,True,BLACK if winner[0] == 'B' else WHITE)


                            self.game_over= True
        
            
            if invalid_move:
                current_time = time.time()
                if current_time - invalid_start >= 1.5:
                    invalid_move = False


            self.screen.fill(BGCOLOR) 
            
            self.board_surface.fill(GREEN)
            x,y = pygame.mouse.get_pos()


            if not self.game_over and (not self.ai or (self.ai and self.user_piece == self.turn)) and pygame.mouse.get_focused() and x <= self.board_width and y >= self.TOP_GAP:

                y -= self.TOP_GAP

                pygame.draw.circle(self.surface,self.transparent_color,(self.square_size//2,self.square_size//2),self.circle_gap)


                self.board_surface.blit(self.surface,(x//self.square_size * self.square_size,y//self.square_size * self.square_size))

            self.screen.blit(self.board_surface,(0,self.TOP_GAP))
            self.draw_board()
            self._draw_score()


            if not self.game_over:
                if not invalid_move:
                    self.screen.blit(self.turn_text,(self.board_width//2 - self.turn_text.get_width()//2,50))
                else:
                    self.screen.blit(self.invalid_text,(self.board_width//2 - self.invalid_text.get_width()//2,50))
            else:
                point = pygame.mouse.get_pos()
                game_buttons.update(point)

                self.screen.blit(winner_text,(self.board_width//2 - winner_text.get_width()//2,50))
                game_buttons.draw(self.screen)

            pygame.display.update()


    def draw_board(self):


        for row in range(self.TOP_GAP,self.screen_height,self.square_size):
            pygame.draw.line(self.screen,BLACK,(0,row),(self.board_width,row))


        for col in range(0,self.board_width + 1,self.square_size):
            pygame.draw.line(self.screen,BLACK,(col,self.TOP_GAP),(col,self.screen_height))


        

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece == 'B':
                    pygame.draw.circle(self.screen,BLACK,(col * self.square_size + self.square_size//2,self.TOP_GAP + row * self.square_size + self.square_size//2),self.square_size//2 - 10)
                elif piece == 'W':
                    pygame.draw.circle(self.screen,WHITE,(col * self.square_size + self.square_size//2,self.TOP_GAP + row * self.square_size + self.square_size//2),self.square_size//2 - 10)
                elif (row,col) in self.valid_moves:
                    pygame.draw.circle(self.screen,RED,(col * self.square_size + self.square_size//2,self.TOP_GAP + row * self.square_size + self.square_size//2),10)








class Menu:
    
    
    title_font = pygame.font.SysFont("calibri",100)
    

    music_file = "mainmenu.ogg"

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
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)
        self.start()

    

    def get_board_size(self):

        
        

        
        button_width,button_height = self.title_font.render("START",True,BLACK).get_width() + 10,100

        start_button = Button(self.screen_width//2 - button_width//2,self.screen_height - 200 - button_height//2,button_width,button_height,"START",BLACK,RED,self.title_font)

        button = pygame.sprite.GroupSingle(start_button)

        

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
        
        def backspace_operation():
            nonlocal user_answer,user_text,width
            if user_answer and user_answer != '|':
                last = user_answer[-1]
                if  last == '|':
                    user_answer = user_answer[:-2]
                else:
                    user_answer = user_answer[:-1]

                user_text = self.title_font.render(user_answer,True,BLACK)
                width = get_true_width()

        
        error_font = pygame.font.SysFont("calibri",40)
        error_message_1 = error_font.render("EVEN SIZED BOARD ONLY!",True,RED)
        error_message_2 = error_font.render("BOARD SIZE AT LEAST 6!",True,RED)
        error_message_3 = error_font.render("ENTER A VALUE FOR BOARD SIZE!",True,RED)

        error = False
        backspace_pressed = False
        errors = []
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
                    elif event.key == pygame.K_BACKSPACE:
                        backspace_operation()



                elif event.type == FLICKERING_EVENT:

                    if user_answer and user_answer[-1] == '|':
                        user_answer = user_answer[:-1]
                    else:
                        user_answer = user_answer + '|'

                    user_text = self.title_font.render(user_answer,True,BLACK)
                    width = get_true_width()
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    point = pygame.mouse.get_pos()
                    collided = True if event.type != pygame.MOUSEBUTTONDOWN else button.sprite.collided_on(point)

                    if collided:
                        if user_answer and user_answer != '|':
                            user_answer = user_answer[:-1] if user_answer[-1] == '|' else user_answer
                            i = int(user_answer)

                            if i % 2:
                                error = True
                                error_message = error_message_1
                                errors.append(error_message_1)

                            if i < 4: #6
                                error = True
                                error_message = error_message_2
                                errors.append(error_message_2)
                        else:
                            error = True
                            errors.append(error_message_3)



                        if error:
                            error_start_time = time.time()
                        else:
                            return i



        
            
            
            point = pygame.mouse.get_pos()
            button.update(point)

            keys_pressed = pygame.key.get_pressed()


            if keys_pressed[pygame.K_BACKSPACE]:
                current_time = time.time()
                if backspace_pressed and current_time - backspace_pressed_start_time >= 0.1:
                    backspace_operation()
                    backspace_pressed_start_time = time.time()
                elif not backspace_pressed:
                    backspace_pressed = True
                    backspace_pressed_start_time = time.time()
            elif backspace_pressed:
                backspace_pressed = False

            

            self.screen.fill(GREEN)
            self.screen.blit(text,text_rect)
            
            if error == True:

                for i,error_message in enumerate(errors):
                    self.screen.blit(error_message,(self.screen_width//2 - error_message.get_width()//2,self.screen_height - 50  - i * (error_message.get_height() + 20)))
                current_time = time.time()
                if current_time - error_start_time >= 2:
                    errors = []
                    error = False

            

            button.draw(self.screen)

             
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


                    
                    for i,button in enumerate(buttons_list):
                        if button.collided_on(point):
                            return i



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
                            mode = self.ai_or_regular_screen()
                            size = self.get_board_size()
                            pygame.display.set_caption(f"OTHELLO {size} x {size}")
                            Game(self.screen,size,size,ai=True if mode==1 else False)
                            pygame.display.set_caption("OTHELLO")
                            self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))




                    

                    

            
            point = pygame.mouse.get_pos()
            self.buttons.update(point)


            self.screen.fill(GREEN)
            self.screen.blit(self.title_text,(self.screen_width//2 - self.title_text.get_width()//2,50))
            self.buttons.draw(self.screen)
            pygame.display.update()


    

class Board:


    def __init__(self,board):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    

    def get_valid_moves(self,current_piece,opposite_piece):

        valid_moves = set()
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    for row_diff in (-1,0,1):
                        for col_diff in (-1,0,1):
                            if row_diff == 0 and col_diff == 0:
                                continue
                            if self_._check(row,col,row_diff,col_diff,current_piece,opposite_piece):
                                valid_moves.add((row,col))

        

        return valid_moves



    def _check(self,row,col,row_diff,col_diff,current_piece,opposite_piece,checking=True):

        
    


        in_bounds = lambda row,col: 0 <= row < self.rows and 0 <= col < self.cols
        

        current_row = row + row_diff
        current_col = col + col_diff



        while in_bounds(current_row,current_col) and self.board[current_row][current_col] == opposite_piece:
            current_row += row_diff
            current_col += col_diff
        
        

        if in_bounds(current_row,current_col) and self.board[current_row][current_col] == current_piece and abs(current_row - row) != 1 and abs(current_col - col) != 1:
        
            if not checking:
                current_row -= row_diff
                current_col -= col_diff

                while current_row != row or current_col != col:
                    self._switch_color(current_row,current_col,user_piece)
                    current_row -= row_diff
                    current_col -= col_diff
            return True

        else:
            return False

    

    def _switch_color(self,row,col,user_piece):
        self.board[row][col] = user_piece


    def _make_move(self,row,col,user_piece,opposite_piece): 


        for row_diff in (-1,0,1):
            for col_diff in (-1,0,1):
                self._check(row,col,row_diff,col_diff,user_piece,opposite_piece,checking=False)



     
    def _no_more_moves(self):
        return not self.get_valid_moves()

    






class GameAI(Game):


    def __init__(self,screen,rows=8,cols=8):
        super().__init__(screen,rows,cols)






        








if __name__ == "__main__":
    
    Menu()






