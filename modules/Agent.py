import numpy as np
from modules.Constants import *

class Agent:
    def __init__(self, position, goal, color, futinobe, middle=False, middle_position=None):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.goal = np.array(goal)
        self.color = color
        self.max_speed = MAX_SPEED
        self.hitosiya = HITO_SIYA_LEVEL
        self.wallsiya = WALL_SIYA_LEVEL
        self.futinobe = futinobe
        self.middle = middle
        if middle:
            self.middle_position = middle_position
        else:
            self.middle_position = None

    def update(self, agents, walls):
        # 目的地に向かう力
        if self.middle and self.middle_position is not None:
            sekkati_level_velocity = (self.middle_position - self.position)
        else:
            sekkati_level_velocity = (self.goal - self.position)
        if np.linalg.norm(sekkati_level_velocity) > 0:
            sekkati_level_velocity = sekkati_level_velocity / np.linalg.norm(sekkati_level_velocity) * self.max_speed
        
        # 衝突回避力（他のエージェントと壁）
        human_avoid_power, wall_avoid_power = self.impact_avoid(agents, walls)
        
        # 速度の更新
        self.velocity += (sekkati_level_velocity - self.velocity) * SEKKATI + human_avoid_power * YASASISA + wall_avoid_power * AVOID_WALL_WEIGHT
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        
        # 位置の更新
        self.position += self.velocity
          # 目的地に近づいたら速度を減少させる
        if np.linalg.norm(self.position - self.goal) < 20:
            self.velocity *= 0.5  # 目的地に近づいたらスピードを落とす
        
        # 中間地点に着いたら目的地を変更
        if self.middle and self.middle_position is not None:
            if np.linalg.norm(self.position - self.middle_position) < 20:
                self.middle_position = None

    def impact_avoid(self, agents, walls):
        human_avoid_power = np.zeros(2) # 初期化
        wall_avoid_power = np.zeros(2) # 初期化

        # -- 他人と回避 --
        for other in agents:
            if other != self: # 自分じゃない
                diff = self.position - other.position
                dist = np.linalg.norm(diff)
                if 0 < dist < self.hitosiya:
                    human_avoid_power += diff / dist * (self.hitosiya - dist) # 他人が近いほど強く回避
        
        # -- 壁との回避 --
        for wall in walls:
            # くりっぷ!!
            closest_point = np.clip(self.position, wall[:2], wall[2:])
            diff = self.position - closest_point
            dist = np.linalg.norm(diff)
            if 0 < dist < self.wallsiya:
                wall_avoid_power += diff / dist * (self.wallsiya - dist)  # 壁が近いほど強く回避
        
        return human_avoid_power, wall_avoid_power