import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from blob import Blob

SIZE = 10
B_DICT = {
    0: "empty",
    1: "player",
    2: "food",
    3: "enemy"
}

class MyEnv(gym.Env):

    def __init__(self, size):
        self.world_size = size
        self.player = Blob(size)
        self.food = Blob(size)
        self.enemy = Blob(size)
        
        self.viewer = None

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=size-1, shape=(3, 2), dtype=np.int)

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.player.action(action)
        
        self.state = None
        step_reward = 0
        done = False

        return self.state, step_reward, done, {}

    def reset(self):
        self.state = self.np_random.randint(low=0, high=self.world_size, size=(3, 2))
        return self.state

    def render(self, mode='human'):
        screen_size = 300
        world_size = self.world_size
        scale = screen_size // world_size

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_size, screen_size)

            player = rendering.FilledPolygon([(0, 0), (0, scale), (scale, scale), (scale, 0)])
            player.set_color(0, 0, 255)
            self.playertrans = rendering.Transform()
            player.add_attr(self.playertrans)
            self.viewer.add_geom(player)

            food = rendering.FilledPolygon(self.food.get_vertices(scale))
            food.set_color(0, 255, 0)
            self.viewer.add_geom(food)

            enemy = rendering.FilledPolygon(self.enemy.get_vertices(scale))
            enemy.set_color(255, 0, 0)
            self.viewer.add_geom(enemy)

        self.playertrans.set_translation(self.player.x*scale, self.player.y*scale)

        return self.viewer.render()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

if __name__ == "__main__":
    env = MyEnv(SIZE)
    env.reset()
    for _ in range(10):
        env.render()
        env.step(env.action_space.sample())
        time.sleep(0.2)
    env.close()
    


    # player = Blob(SIZE)
    # food = Blob(SIZE)
    # enemy = Blob(SIZE)

    # img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    # img[food.x][food.y] = (0, 255, 0)
    # img[player.x][player.y] = (255, 0, 0)
    # img[enemy.x][enemy.y] = (0, 0, 255)
    # img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_NEAREST)

    # cv2.imshow("image", img)
    # cv2.waitKey(0)