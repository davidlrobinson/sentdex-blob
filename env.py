import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from blob import Blob

SIZE = 10

N_EPISODES = 10
MOVE_REWARD = -1
ENEMY_REWARD = -300
FOOD_REWARD = 25
SHOW_EVERY = 1

class BlobEnv(gym.Env):

    def __init__(self, size):
        self.seed()

        self.world_size = size
        self.player = Blob(self.np_random, size)
        self.food = Blob(self.np_random, size)
        self.enemy = Blob(self.np_random, size)
        
        self.viewer = None

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=size-1, shape=(3, 2), dtype=np.int)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.player.action(action)
        self.enemy.move()
        
        self.state = np.array([self.player.pos, self.food.pos, self.enemy.pos])
        if self.player.pos == self.enemy.pos:
            reward = ENEMY_REWARD
            done = True
        elif self.player.pos == self.food.pos:
            reward = FOOD_REWARD
            done = True
        else:
            reward = MOVE_REWARD
            done = False

        return self.state, reward, done, {}

    def reset(self):
        self.player.reset(), self.food.reset(), self.enemy.reset()
        self.state = np.array([self.player.pos, self.food.pos, self.enemy.pos])
        return self.state

    def render(self, mode='human'):
        screen_size = 300
        world_size = self.world_size
        scale = screen_size // world_size
        blob_vertices = [(0, 0), (0, scale), (scale, scale), (scale, 0)]

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_size, screen_size)

            player = rendering.FilledPolygon(blob_vertices)
            player.set_color(0, 0, 255)
            self.playertrans = rendering.Transform()
            player.add_attr(self.playertrans)
            self.viewer.add_geom(player)

            food = rendering.FilledPolygon(blob_vertices)
            food.set_color(0, 255, 0)
            self.foodtrans = rendering.Transform()
            food.add_attr(self.foodtrans)
            self.viewer.add_geom(food)

            enemy = rendering.FilledPolygon(blob_vertices)
            enemy.set_color(255, 0, 0)
            self.enemytrans = rendering.Transform()
            enemy.add_attr(self.enemytrans)
            self.viewer.add_geom(enemy)

        self.playertrans.set_translation(self.player.x*scale, self.player.y*scale)
        self.foodtrans.set_translation(self.food.x*scale, self.food.y*scale)
        self.enemytrans.set_translation(self.enemy.x*scale, self.enemy.y*scale)

        return self.viewer.render()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

if __name__ == "__main__":
    env = BlobEnv(SIZE)
    for i in range(N_EPISODES):
        env.reset()
        for t in range(200):
            if i % SHOW_EVERY == 0:
                env.render()
            observation, reward, done, info = env.step(env.action_space.sample())
            if done:
                print("Episode {} finished after {} timesteps".format(i+1, t+1))
                break
    env.close()