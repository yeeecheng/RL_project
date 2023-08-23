import pygame
from collections import namedtuple

Size = namedtuple("Size","w,h")
Pos = namedtuple("Pos","x, y")

BLOCK_SIZE = Size(25, 25)
SCREEN_SIZE = Size(500, 500)
SPEED = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Maze1D():
    
    def __init__(self):
        
        # render setting 
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Maze1D") 
        
        self.screen.fill(BLACK)
        
        self.render_player = pygame.Surface(BLOCK_SIZE)
        self.render_player.fill(color= GREEN)

        self.render_black = pygame.Surface(BLOCK_SIZE)
        self.render_black.fill(color= BLACK)

        self.font = pygame.font.SysFont("simhei", 24)
        # speed setting 
        self.fps = pygame.time.Clock()

        self.reset()
    
    def reset(self):
        
        # param setting
        self.player_pos =  Pos(0, 250)
        self.goal_pos = Pos(SCREEN_SIZE.w - BLOCK_SIZE.w, 250)
        self.frame_steps = 0 
        self.game_over = False

    def __update_UI(self):
        
        self.screen.fill(BLACK)
        self.screen.blit(self.render_player,self.player_pos)
        self.screen.blit(self.font.render(f"step {self.frame_steps}", True, WHITE, BLACK),(20,20))
        pygame.display.update()

    def __is_collision(self, pos:Pos)->bool:
        if pos.x < 0 or pos.x >= SCREEN_SIZE.w \
            or pos.y < 0 or pos.y >= SCREEN_SIZE.h:
            return True

        return False

    def __move(self,action):
        """
        action :
        0 -> left movement
        1 -> no movement
        2 -> right movement
        """
        mx, my = 0, 0
        if action != 1:
            mx = -BLOCK_SIZE.w if action == 0 else BLOCK_SIZE.w
        
        self.player_pos= Pos(self.player_pos.x + mx, self.player_pos.y + my) 
    
    def get_player_current_pos(self):
        return self.player_pos.x // BLOCK_SIZE.w

    def step(self, action:list)->[int, bool, int]:
        
        reward = 0
        self.frame_steps += 1
        self.fps.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
        self.__move(action= action)
        if self.__is_collision(self.player_pos) or self.frame_steps >= 200:
            reward  = -10
            self.game_over = True
            return reward, self.game_over, self.frame_steps
        if self.player_pos == self.goal_pos:
            reward = 10
            self.game_over = True
            return reward,  self.game_over, self.frame_steps

        self.__update_UI()

        return reward, self.game_over, self.frame_steps 
    
if __name__ == "__main__":
    env = Maze1D()
