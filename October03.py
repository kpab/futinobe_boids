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
        self.max_speed = 3.0
        self.perception_radius = 20.0

    def update(self, agents, walls):
        # 目的地に向かう力
        desired_velocity = (self.destination - self.position)
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
                avoidance_force += diff / dist * (self.perception_radius - dist) 
        
        return avoidance_force

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        self.walls = []
        self.start_positions = []
        self.destinations = []
        self.destination_weights = []
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']

    def add_wall(self, x1, y1, x2, y2):
        self.walls.append((x1, y1, x2, y2))

    def add_start_position(self, x, y):
        self.start_positions.append((x, y))

    def add_destination(self, x, y, weight):
        self.destinations.append((x, y))
        self.destination_weights.append(weight)

    def generate_agent(self):
        if not self.start_positions or not self.destinations:
            return

        start_position = self.start_positions[np.random.randint(len(self.start_positions))]
        destination_index = np.random.choice(len(self.destinations), p=np.array(self.destination_weights) / sum(self.destination_weights))
        destination = self.destinations[destination_index]
        color = self.colors[destination_index % len(self.colors)]
        
        self.agents.append(Agent(start_position, destination, color))

    def update(self):
        for agent in self.agents:
            agent.update(self.agents, self.walls)
        self.agents = [agent for agent in self.agents if np.linalg.norm(agent.position - agent.destination) > 5]
        if np.random.rand() < 0.1:  # 10%の確率で新しいエージェントを生成
            self.generate_agent()

    def animate(self, num_frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # 壁の描画
        for wall in self.walls:
            ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1]))

        # 目的地の描画
        for dest in self.destinations:
            ax.plot(dest[0], dest[1], 'k*', markersize=5)

        # スタート位置の描画
        for start in self.start_positions:
            ax.plot(start[0], start[1], 'go', markersize=5)

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

sim.add_wall(475, 390, 500, 395)
sim.add_wall(475, 370, 500, 375)
sim.add_wall(475, 350, 500, 355)

# スタート位置の追加
sim.add_start_position(480, 260)
sim.add_start_position(480, 280)
sim.add_start_position(480, 300)
sim.add_start_position(250, 450)

# 目的地の追加（重みつき）
# sim.add_destination(480, 320, 0.1)  # 40%の確率
# sim.add_destination(480, 340, 0.1)
# sim.add_destination(480, 360, 0.1)
# sim.add_destination(480, 380, 0.1)
sim.add_destination(470, 320, 0.1)  # 40%の確率
sim.add_destination(470, 340, 0.1)
sim.add_destination(470, 360, 0.1)
sim.add_destination(470, 380, 0.1)

sim.add_destination(55, 430, 0.1) 
sim.add_destination(55, 440, 0.1)
sim.add_destination(55, 450, 0.1) 
sim.add_destination(250, 250, 0.2)  # 20%の確率

# 初期エージェントの生成
for _ in range(50):
    sim.generate_agent()

# アニメーションの実行
sim.animate(500)