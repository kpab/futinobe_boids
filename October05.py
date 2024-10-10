'''
迷惑系の修正
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

FRAME_COUNT = 500
START_HUMAN_COUNT = 10 # 初期
SIYA_LEVEL = 20.0 # 👁️
MAX_SPEED = 2.0 # 🦵
BORN_RATE = 0.5
SEKKATI = 0.2
YASASISA = 0.4



class Agent:
    def __init__(self, position, goal, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.goal = np.array(goal)
        self.color = color
        self.max_speed = MAX_SPEED
        self.siya = SIYA_LEVEL

    def update(self, agents, walls):
        # 目的地に向かう力
        sekkati_level_velocity = (self.goal - self.position)
        if np.linalg.norm(sekkati_level_velocity) > 0:
            sekkati_level_velocity = sekkati_level_velocity / np.linalg.norm(sekkati_level_velocity) * self.max_speed
        
        # 衝突回避力（他のエージェントと壁）
        avoid_power = self.impact_avoid(agents, walls) * 0.5
        
        # 速度の更新
        self.velocity += (sekkati_level_velocity - self.velocity) * SEKKATI + avoid_power * YASASISA
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        
        # 位置の更新
        self.position += self.velocity
          # 目的地に近づいたら速度を減少させる
        if np.linalg.norm(self.position - self.goal) < 20:
            self.velocity *= 0.5  # 目的地に近づいたらスピードを落とす

    def impact_avoid(self, agents, walls):
        avoid_power = np.zeros(2) # 初期化
        
        # -- 他人と回避 --
        for other in agents:
            if other != self: # 自分じゃない
                diff = self.position - other.position
                dist = np.linalg.norm(diff)
                if 0 < dist < self.siya:
                    avoid_power += diff / dist * (self.siya - dist) # 他人が近いほど強く回避
        
        # -- 壁との回避 --
        for wall in walls:
            # くりっぷ!!
            closest_point = np.clip(self.position, wall[:2], wall[2:])
            diff = self.position - closest_point
            dist = np.linalg.norm(diff)
            if 0 < dist < self.siya:
                avoid_power += diff / dist * (self.siya - dist)  # 壁が近いほど強く回避
        
        return avoid_power

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        self.walls = []
        self.fake_walls = []
        self.start_positions = []
        self.goals = []
        self.goal_weights = []
        self.colors = ['red', 'blue', 'green', 'pink', 'purple']

    def add_wall(self, x1, y1, x2, y2):
        self.walls.append((x1, y1, x2, y2))

    def add_fake_wall(self, x1, y1, x2, y2):
        self.fake_walls.append((x1, y1, x2, y2))

    def add_start_position(self, x, y):
        self.start_positions.append((x, y))

    def add_goal(self, x, y, weight):
        self.goals.append((x, y))
        self.goal_weights.append(weight)

    def born_agent(self):
        if not self.start_positions or not self.goals:
            return

        start_position = self.start_positions[np.random.randint(len(self.start_positions))]
        goal_index = np.random.choice(len(self.goals), p=np.array(self.goal_weights) / sum(self.goal_weights))
        goal = self.goals[goal_index]
        color = self.colors[goal_index % len(self.colors)]
        
        self.agents.append(Agent(start_position, goal, color))

    def update(self):
        for agent in self.agents:
            agent.update(self.agents, self.walls)
     
        self.agents = [agent for agent in self.agents if np.linalg.norm(agent.position - agent.goal) > 15]
        if np.random.rand() < BORN_RATE:  # 確率で新しいエージェントを生成
            self.born_agent()

    def animate(self, num_frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # 壁の描画
        for wall in self.walls:
            ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1]))

        for wall in self.fake_walls:
            # ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1]))
            ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1],fc="r"))

        # 目的地の描画
        for dest in self.goals:
            ax.plot(dest[0], dest[1], 'k*', markersize=10)

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
sim.add_wall(0, 0, 30, 500) # 左
sim.add_wall(485, 0, 500, 500) # 右
sim.add_wall(0, 450, 500, 500) # 上
sim.add_wall(0, 0, 500, 150) # 下
sim.add_wall(0, 0, 300, 300) # 左下

sim.add_wall(250, 370, 300, 450)
sim.add_wall(50, 300, 150, 320)

# フェイク壁
sim.add_fake_wall(475, 0, 500, 500)
sim.add_fake_wall(30,300, 50, 450)

# スタート位置の追加
sim.add_start_position(470, 200)
sim.add_start_position(470, 220)
sim.add_start_position(470, 240)


sim.add_start_position(55, 440) 
sim.add_start_position(55, 420) 

# エスカレーター(上り)
sim.add_start_position(310, 440) 
sim.add_start_position(310, 420) 

# 階段(右)
sim.add_start_position(470, 440) 
sim.add_start_position(470, 420) 
sim.add_start_position(470, 400) 
sim.add_start_position(470, 380) 


# 目的地(確率あり）

sim.add_goal(470, 260, 0.1)  # 40%の確率
sim.add_goal(470, 280, 0.1)
sim.add_goal(470, 300, 0.2)
sim.add_goal(470, 320, 0.2)

sim.add_goal(55, 400, 0.1) 
sim.add_goal(55, 380, 0.1) 

# エスカレーター(下り)
sim.add_goal(310, 400, 0.1) 
sim.add_goal(310, 380, 0.1) 



# 初期エージェントの生成
for _ in range(START_HUMAN_COUNT):
    sim.born_agent()

# アニメーションの実行
sim.animate(FRAME_COUNT)