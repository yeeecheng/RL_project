import torch
import random
import numpy as np 
from collections import deque
from snake_game import snakeGame, Pos
from model import Linear_QNet, QTrainer
from helper import plot

import time
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent():

    def __init__(self,test = False):
        
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3) 
        self.trainer = QTrainer(self.model, lr=LR, gamma= self.gamma)
        self.test = test


    def get_state(self, game):
        
        head = game.snake[0]
        action_move = game.get_action_move()
        direction = game.direction
        # r, d, l, u
        point_dir = [Pos(head.x + mx, head.y + my)  for mx, my in action_move]
        dir = [game.snake_direction == dir for dir in direction]

        idx = dir.index(True)

        state = [

            dir[idx] and game.is_collision(point_dir[idx].x , point_dir[idx].y),
            dir[idx] and game.is_collision(point_dir[(idx + 1) % 4].x, point_dir[(idx + 1) % 4].y),
            dir[idx] and game.is_collision(point_dir[(idx + 3) % 4].x, point_dir[(idx + 3) % 4].y),
            
            dir[0],
            dir[1],
            dir[2],
            dir[3],

            game.food_pos.x < game.head_pos.x,
            game.food_pos.x > game.head_pos.x,
            game.food_pos.y < game.head_pos.y,
            game.food_pos.y > game.head_pos.y,
        ]
        
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #     self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        
        if self.test:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

            return final_move

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = snakeGame()
    
    while True:

        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)
        
        reward, done, score = game.step(action = final_move)
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state = state_old, action = final_move, reward = reward, next_state = state_new, done = done)

        agent.remember(state = state_old, action = final_move, reward = reward, next_state = state_new, done = done)
        
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score 
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(scores = plot_scores, mean_scores = plot_mean_scores)


def test():

    agent = Agent(test=True)
    game = snakeGame()

    agent.model.load_state_dict(torch.load("./model/model.pth"))
    agent.model.eval()
    while True:
        state = agent.get_state(game)
        final_move = agent.get_action(state)
        
        reward, done, score = game.step(action = final_move)

        if done :
            return
        
if __name__ == "__main__":
    # train()
    test()


