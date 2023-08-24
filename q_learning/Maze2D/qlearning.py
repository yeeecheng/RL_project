from env import Maze2D
import pandas as pd
import numpy as np
import random
from tqdm import tqdm

class Q_learning():

    def __init__(self,env, episode= 200, gamma= 0.9, alpha= 0.1, epsilon=0.9):
        
        self.env = env
        self.episode = episode
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        # stand l, u , r, d
        self.action_list = [0, 1, 2, 3, 4]
        # create qtable
        self.qtable = pd.DataFrame(columns= self.action_list)

    def __check_state_exist(self,state):
        
        if state not in self.qtable.index:
            new_state = pd.DataFrame(np.zeros((1, len(self.action_list))),columns= self.action_list, index=[state])
            self.qtable = pd.concat([self.qtable, new_state])
        

    def __choose_action(self, state):
        
        self.__check_state_exist(state)
        action = random.randint(0, 4)
        if random.uniform(0, 1) <= self.epsilon:

            # 要打亂順序， 否則當有多個最大值，都只會找第一個
            max_ele = [idx for idx, ele in enumerate(self.qtable.loc[state]) if ele == self.qtable.loc[state].max()]
            action = random.choice(max_ele)

        return action 
    
    def __update_qtable(self,s, action, reward, s_, done):
        
        self.__check_state_exist(state= s_)
        q_predict = self.qtable.loc[s][action]
        q_target = reward
        if not done:
            q_target += self.gamma * self.qtable.loc[s_].max()

        self.qtable.loc[s][action] = q_predict + self.alpha * (q_target - q_predict)


    def train(self):

        progress_bar = tqdm(range(self.episode))
        for _ in progress_bar:

            while True:
                s = self.env.get_current_state()
                action = self.__choose_action(state= s)
                reward, done, steps = self.env.step(action= action)
                progress_bar.set_description(f"steps: {steps}")
                s_ = self.env.get_current_state()
                self.__update_qtable(s= s, action= action, reward= reward, s_= s_, done= done)

                if done:
                    self.env.reset()
                    break
        self.env.destroy_render()

if __name__ == "__main__":
    
    qlearning = Q_learning(env= Maze2D(), episode=300)
    qlearning.train()
