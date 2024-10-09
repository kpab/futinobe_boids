import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

class Agent:
    def __init__(self, position, destination, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.destination = np.array(destination)
        self.color = color
        self.max_speed = 6.0

    def update(self):
        # 目的地に向かう力
        desired_velocity = (self.destination - self.position)
        if np.linalg.norm(desired_velocity) > 0:
            desired_velocity = desired_velocity / np.linalg.norm(desired_velocity) * self.max_speed
       
        
        # 速度の更新
        self.velocity += (desired_velocity - self.velocity)
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        
        # 位置の更新
        self.position += self.velocity


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        self.walls = []
        self.destinations = []
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']

    def add_destination(self, x, y):
        self.destinations.append((x, y))

    def generate_agent(self):
        position = np.random.rand(2) * [self.width, self.height]
        destination = self.destinations[np.random.randint(len(self.destinations))]
        color = self.colors[self.destinations.index(destination)]
        self.agents.append(Agent(position, destination, color))

    def update(self):
        for agent in self.agents:
            agent.update()
        self.agents = [agent for agent in self.agents if np.linalg.norm(agent.position - agent.destination) > 5]
        if np.random.rand() < 0.9:  # 10%の確率で新しいエージェントを生成
            self.generate_agent()

    def animate(self, num_frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # 目的地の描画
        for dest in self.destinations:
            ax.plot(dest[0], dest[1], 'k*', markersize=10)

        scatter = ax.scatter([], [], c=[])

        def update(frame):
            self.update()
            scatter.set_offsets(np.array([agent.position for agent in self.agents]))
            scatter.set_color([agent.color for agent in self.agents])
            return scatter,

        anim = FuncAnimation(fig, update, frames=num_frames, interval=50, blit=True)
        plt.show()

# シミュレーションの設定
sim = Simulation(500, 500)


# 目的地の追加
for _ in range(5):
    sim.add_destination(np.random.rand() * 500, np.random.rand() * 500)

# 初期エージェントの生成
for _ in range(50):
    sim.generate_agent()

# アニメーションの実行
sim.animate(500)