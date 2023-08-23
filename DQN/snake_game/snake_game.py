import pygame
from collections import namedtuple
import random
import numpy as np

# RGB color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# direction
RIGHT = 0
DOWN  = 1
LEFT  = 2
UP    = 3


Size = namedtuple("Size", "w, h")
Pos = namedtuple("Pos", "x, y")

BLOCK_SIZE = Size(30, 30)
SCREEN_SIZE = Size(660, 660)
BOARD_SIZE = Size(30, 30)
BOARD_WIDTH = 2
SPEED = 120

class snakeGame():

    def __init__(self):
        
        self.direction = [RIGHT, DOWN, LEFT, UP]
        # movement, up, down, left, right
        self.action_move = [[BLOCK_SIZE.w, 0], [0, BLOCK_SIZE.h], [-BLOCK_SIZE.w, 0], [0, -BLOCK_SIZE.h]]
        pygame.init()
        
        # create window screen
        self.render_screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("snake game")
        
        # create background
        self.bg = pygame.Surface(self.render_screen.get_size()).convert()
        self.bg.fill(BLACK)
        pygame.draw.rect(self.bg, WHITE, [BOARD_SIZE.w - BOARD_WIDTH, BOARD_SIZE.h - BOARD_WIDTH,\
                                     SCREEN_SIZE.w - (BOARD_SIZE.w - BOARD_WIDTH) * 2,\
                                     SCREEN_SIZE.h - (BOARD_SIZE.h - BOARD_WIDTH) * 2], BOARD_WIDTH)
        # create render snake
        self.render_snake = pygame.Surface(BLOCK_SIZE)
        self.render_snake.fill(GREEN)

        # create render food
        self.render_food = pygame.Surface(BLOCK_SIZE)
        self.render_food.fill(RED)

        # create black obj
        self.render_black = pygame.Surface(BLOCK_SIZE)
        self.render_black.fill(BLACK)

        # create show text
        self.font = pygame.font.SysFont("simhei", 24)

        # speed
        self.fps = pygame.time.Clock()
        
        self.reset()    

    
    def reset(self):
        
        # snake
        self.snake_direction = RIGHT
        self.head_pos = Pos(SCREEN_SIZE.w // 2, SCREEN_SIZE.h // 2)
        self.snake = [self.head_pos,
                    Pos(self.head_pos.x - BLOCK_SIZE.w, self.head_pos.y),
                    Pos(self.head_pos.x - 2 * BLOCK_SIZE.w, self.head_pos.y)]

        self.food_pos = self.__get_food_new_position()
        
        self.score = 0
        self.game_over = False
        self.frame_iteration = 0

        self.__update_UI(first = True)

    def __update_UI(self,first = False, eat_food = False):
        
        if first:
            
            self.render_screen.blit(self.bg, (0, 0))
            for pos in self.snake:
                self.render_screen.blit(self.render_snake, pos)
            self.render_screen.blit(self.render_food, self.food_pos)
            self.render_screen.blit(self.font.render("Score: 0", True, WHITE, BLACK), (30, 640))
            pygame.display.update()

            return 
        
        if eat_food:
            self.render_screen.blit(self.render_black, self.prev_food_pos)
            self.render_screen.blit(self.render_food, self.food_pos)
            self.render_screen.blit(self.font.render(f"Score: {self.score}", True, WHITE, BLACK), (30, 640))
        elif not first:
            
            self.render_screen.blit(self.render_black, self.prev_snake_pos)
        
        self.render_screen.blit(self.render_snake, self.head_pos)
        
        # update
        pygame.display.update()

    def __get_random_position(self)->[int, int]:

        x = (random.randint(BOARD_SIZE.w // BLOCK_SIZE.h, \
                        (SCREEN_SIZE.w - BOARD_SIZE.w) // BLOCK_SIZE.w - 1)) * BLOCK_SIZE.w
        y = (random.randint(BOARD_SIZE.h // BLOCK_SIZE.h, \
                            (SCREEN_SIZE.h - BOARD_SIZE.h) // BLOCK_SIZE.h - 1)) * BLOCK_SIZE.h
        
        return x , y

    def __get_food_new_position(self, x = None, y = None)->tuple[int, int]:
        
        new_x, new_y = self.__get_random_position()

        if Pos(new_x, new_y) in self.snake:
            return self.__get_food_new_position(x, y)
        
        self.prev_food_pos = Pos(x, y)
        
        return Pos(new_x, new_y)
    
    def step(self,action):

        self.fps.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.frame_iteration += 1
        
        self.__move(action=action)
        
        reward = 0
        if self.is_collision(self.head_pos.x, self.head_pos.y) or self.frame_iteration > 100 * len(self.snake):    
            self.game_over = True
            reward = -10
            return reward, self.game_over, self.score
        
        self.snake.insert(0, self.head_pos)
        self.prev_snake_pos = self.snake[-1]

        # eat food
        eat_food = False
        if self.head_pos.x == self.food_pos.x and self.head_pos.y == self.food_pos.y:
            self.food_pos = (self.__get_food_new_position(x = self.food_pos.x, y = self.food_pos.y))
            self.score += 1
            eat_food = True
            reward = 10
        else :
            # remove prev tail
            self.snake.pop()
        
        self.__update_UI(eat_food = eat_food)

        return reward, self.game_over, self.score

    def __move(self,action):
        
        """
        # direction
        RIGHT = 0
        DOWN  = 1
        LEFT  = 2
        UP    = 3

        [1, 0, 0]: straight
        [0, 1, 0]: right turn
        [0, 0, 1]: left turn
        """
        
        clock_wise = [RIGHT, DOWN, LEFT, UP]
        idx = clock_wise.index(self.snake_direction)

        if not np.array_equal(action, [1, 0, 0]):
            idx = (idx + 1) % 4 if np.array_equal(action, [0, 1, 0]) else (idx + 3) % 4
        self.snake_direction = clock_wise[idx]
        mx, my = self.action_move[self.snake_direction]

        self.head_pos = Pos(self.head_pos.x + mx, self.head_pos.y + my)
    
    def is_collision(self, x, y)->bool:
        if x  < BOARD_SIZE.w or x  >= (SCREEN_SIZE.w - BOARD_SIZE.w) \
            or y  < BOARD_SIZE.h or y  >= (SCREEN_SIZE.h - BOARD_SIZE.h) \
            or Pos(x, y) in self.snake :
            return True
        
        return False
    
    def is_game_over(self)->bool:
        return self.game_over
    
    def get_action_move(self):
        return self.action_move

if __name__ == "__main__":

    game = snakeGame()
    game_over = False
    action = [[1,0,0],[0,0,1],[0,0,1]]
    while not game.is_game_over():
        r = random.randint(0,2)
        game.step(action=action[r])
