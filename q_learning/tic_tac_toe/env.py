import pygame
from collections import namedtuple
import time
import random 

Size = namedtuple("Size","w,h")

BLOCK_SIZE = Size(100, 100)
SCREEN_SIZE = Size(500, 500)
SPEED = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
BLUE = (0, 0, 255)



class Tic_Tac_Toe():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Tic-Tac-Toe")

        self.screen.fill(WHITE)
        self.__create_bg()
        self.__update_UI()
        time.sleep(4)
    
    def __create_bg(self):
        
        pygame.draw.line(self.screen, BLACK, (200, 100), (200, 400))
        pygame.draw.line(self.screen, BLACK, (300, 100), (300, 400))   
        pygame.draw.line(self.screen, BLACK, (100, 200), (400, 200))
        pygame.draw.line(self.screen, BLACK, (100, 300), (400, 300))

    def reset(self):
        
        # choose one player to stare game
        self.current_player = random.randint(1,2)
        # create new game board
        # -1 : no player choose
        # 1 : player 1
        # 2 : player 2
        self.board = [[-1 for _ in range(3)] for _ in range(3)] 

        self.game_over = False
    
    def __check_game_over(self, player)->bool:
        

        for i in range(3):
            if self.board[i].count(player) == 3:
                return True

    def step(self):
        pass

    def __update_UI(self):
        pygame.display.update()

    def __move(self):
        pass


if __name__ == "__main__":
    env = Tic_Tac_Toe()