import pygame
from collections import namedtuple
import time

Size = namedtuple("Size","w,h")
Pos = namedtuple("Pos","x, y")

BLOCK_SIZE = Size(50, 50)
SCREEN_SIZE = Size(500, 500)
SPEED = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Maze2D():
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Maze2D")
        self.screen.fill(WHITE)

        self.render_player = pygame.Surface(BLOCK_SIZE)
        self.render_player.fill(RED)

        self.render_obstacle = pygame.Surface(BLOCK_SIZE)
        self.render_obstacle.fill(BLACK)

        self.render_goal = pygame.Surface(BLOCK_SIZE)
        self.render_goal.fill(GREEN)

        self.fps = pygame.time.Clock()

        self.reset()

    def __create_bg(self):
        for i in range(SCREEN_SIZE.w // BLOCK_SIZE.w):     
            for j in range(SCREEN_SIZE.h // BLOCK_SIZE.h):
                pygame.draw.rect(self.screen, BLACK, [BLOCK_SIZE.w * i, BLOCK_SIZE.h * j, BLOCK_SIZE.w, BLOCK_SIZE.h], 1)

    def reset(self):
        
        self.player_pos = Pos(0,0)
        self.goal_pos = Pos(450, 450)
        self.obstacle_pos = [Pos(50, 50), Pos(100, 100), Pos(150, 150), Pos(300, 300), Pos(350, 400), Pos(400, 50)]
        self.frame_steps = 0
        self.done = False
        self.__update_UI()

    # return state, reward, done
    def step(self, action):
        
        self.frame_steps += 1
        reward = 0 
        self.fps.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.__move(action= action)
        if self.__is_collision(self.player_pos):
            reward = -10
            self.done = True
            self.__update_UI()
            return reward, self.done, self.frame_steps

        if self.player_pos == self.goal_pos:
            reward = 10
            self.done = True

        self.__update_UI()
        return reward, self.done, self.frame_steps

    def get_current_state(self):
        return f"{self.player_pos.x // BLOCK_SIZE.w}_{self.player_pos.y // BLOCK_SIZE.h}"

    def destroy_render(self):
        pygame.quit()

    def __is_collision(self, pos) -> bool:
        
        if pos.x < 0 or pos.x >= SCREEN_SIZE.w or pos.y < 0 or pos.y >= SCREEN_SIZE.h\
            or pos in self.obstacle_pos:
            return True
        
        return False

    def __update_UI(self):
        
        self.screen.fill(WHITE)
        self.__create_bg()
        self.screen.blit(self.render_goal, self.goal_pos)
        for ob_pos in self.obstacle_pos:
            self.screen.blit(self.render_obstacle, ob_pos)
        self.screen.blit(self.render_player, self.player_pos)

        pygame.display.update()


    def __move(self, action):
        """
        action of movement:
            0 : stand,
            1 : left,
            2 : up,
            3 : right, 
            4 : down
        """

        action_movement = [(0, 0), (-BLOCK_SIZE.w, 0), (0, -BLOCK_SIZE.h), (BLOCK_SIZE.w, 0), (0, BLOCK_SIZE.h)]
        mx, my = action_movement[action]
        self.player_pos = Pos(self.player_pos.x + mx, self.player_pos.y + my)


if __name__ == "__main__":
    env = Maze2D()



