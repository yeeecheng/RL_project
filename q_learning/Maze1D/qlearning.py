from env import Maze1D
import pandas as pd 
import numpy as np
import random


class QLearning():

    def __init__(self, env, episodes):
        
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.9
        self.env = env
        self.episodes = episodes
        # left, stand, right
        self.actions = [0, 1, 2]
        
        self.__reset()

    def __reset(self):
        self.__build_Qtable(n_states= 20, actions= self.actions)
        

    def __build_Qtable(self, n_states, actions):
        """
        The size of Qtable is depending on state and action 
        """
        
        self.q_table = pd.DataFrame(
            np.zeros((n_states, len(actions))),
            columns= actions
            )


    def __choose_action(self,state)->list:
        
        
        state_action = self.q_table.iloc[state, :]
        if random.uniform(0,1) > self.epsilon or state_action.all() == 0:
            action = random.randint(0,2)
        else :
            action = state_action.argmax()
        
        return action
    
    def __update_Qtable(self, state, action, reward, next_state, done):
        
        q_predict = self.q_table.iloc[state][action]
        q_target = reward
        if not done:
            q_target = reward + self.gamma * self.q_table.iloc[next_state].max()
        self.q_table.iloc[state][action] = q_predict + self.alpha * (q_target - q_predict)


    def train(self):

        for episode in range(self.episodes):
            print(f"episode: {episode}")
            while True:
                state_old = self.env.get_player_current_pos()
                action = self.__choose_action(state= state_old)
                
                reward,  done, frame_steps = self.env.step(action= action)
                state_new = self.env.get_player_current_pos()
                self.__update_Qtable(state= state_old, action= action, reward= reward, next_state= state_new, done= done)
                
                if done:
                    print(reward)
                    self.env.reset()
                    break


if __name__ == "__main__":

    rl = QLearning(env= Maze1D(), episodes= 200)
    rl.train()