import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import pandas as pd

class Agent:
    def __init__(self, position, goal, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.goal = np.array(goal)
        self.color = color
        self.max_speed = 3.0
        self.perception_radius = 20.0

    def update(self, agents, walls):
        # 目的地に向かう力
        desired_velocity = (self.goal - self.position)
        if np.linalg.norm(desired_velocity) > 0:
            desired_velocity = desired_velocity / np.linalg.norm(desired_velocity) * self.max_speed
        
        # 衝突回避力（他のエージェントと壁）
        avoidance_force = self.compute_avoidance_force(agents, walls)
        
        # 速度の更新
        self.velocity += (desired_velocity - self.velocity) * 0.1 + avoidance_force
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        
        # 位置の更新
        self.position += self.velocity

    def compute_avoidance_force(self, agents, walls):
        avoidance_force = np.zeros(2)
        
        # エージェント間の回避
        for other in agents:
            if other != self:
                diff = self.position - other.position
                dist = np.linalg.norm(diff)
                if 0 < dist < self.perception_radius:
                    avoidance_force += diff / dist * (self.perception_radius - dist)
        
        # 壁との回避
        for wall in walls:
            closest_point = np.clip(self.position, wall[:2], wall[2:])
            diff = self.position - closest_point
            dist = np.linalg.norm(diff)
            if 0 < dist < self.perception_radius:
                avoidance_force += diff / dist * (self.perception_radius - dist) * 2
        
        return avoidance_force

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        self.walls = []
        self.goals = []
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']

    def add_wall(self, x1, y1, x2, y2):
        self.walls.append((x1, y1, x2, y2))

    def add_goal(self, x, y):
        self.goals.append((x, y))

    def generate_agent(self):
        position = np.random.rand(2) * [self.width, self.height]
        goal = self.goals[np.random.randint(len(self.goals))]
        color = self.colors[self.goals.index(goal)]
        self.agents.append(Agent(position, goal, color))

    def update(self):
        for agent in self.agents:
            agent.update(self.agents, self.walls)
        self.agents = [agent for agent in self.agents if np.linalg.norm(agent.position - agent.goal) > 5]
        if np.random.rand() < 0.1:  # 10%の確率で新しいエージェントを生成
            self.generate_agent()

    def animate(self, num_frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # 壁の描画
        for wall in self.walls:
            ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1], fill=False))

        # 目的地の描画
        for dest in self.goals:
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

# 壁の追加
sim.add_wall(0, 0, 50, 500) # 左
sim.add_wall(485, 0, 500, 500) # 右
sim.add_wall(0, 450, 500, 500) # 上
sim.add_wall(0, 0, 500, 150) # 下
# sim.add_wall(100, 100, 400, 150)
# sim.add_wall(200, 300, 250, 450)

red_goals = []
blue_goals = [[],[],[],[],[],[]]
# 目的地の追加
for _ in range(5):
    
    sim.add_goal(np.random.rand() * 500, np.random.rand() * 500)

# 初期エージェントの生成
for _ in range(50):
    sim.generate_agent()

# アニメーションの実行
sim.animate(500)