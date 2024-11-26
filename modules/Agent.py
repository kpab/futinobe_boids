'''
10/24 目的地に近づくほど減速
10/27 中間地点認識範囲(middle_range)
10/27 目的地に近づくほど減速(SLOW_LEVELの実装)
11/04 速度に幅を持たせる
'''
import random
import numpy as np
from modules.Constants_morning import *

class Agent:
    def __init__(self, position, goal, color, futinobe, middle=False, middle_position=None):
        self.position = np.array(position, dtype=float)
        # self.position = np.array(position, dtype=float).reshape(1, 2)

        self.velocity = np.zeros(2)
        self.goal = np.array(goal)
        self.color = color
        # -- 最高速度設定 --
        if random.random() < MAX_MAX_SPEED[1]:
            self.max_speed= MAX_MAX_SPEED[0]  # 上振れ速度に設定
        elif random.random() < MIN_MAX_SPEED[1]:
            self.max_speed = MIN_MAX_SPEED[0]  # 下振れ速度に設定
        else:
            self.max_speed = MAX_SPEED  # 通常の最高速度にリセット

        self.hitosiya = HITO_SIYA_LEVEL
        self.wallsiya = WALL_SIYA_LEVEL
        self.futinobe = futinobe
        self.middle = middle
        self.frame = 0 # フレーム
        if middle:
            self.middle_position = middle_position
        else:
            self.middle_position = None
        self.total_speed = 0
        

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
        
        # フレームの更新
        self.frame += 1
        self.total_speed += np.linalg.norm(self.velocity)

          # 目的地に近づいたら速度を減少させる
        if np.linalg.norm(self.position - self.goal) < SLOWING_RANGE:
            self.velocity *= (np.linalg.norm(self.position - self.goal))/(SLOWING_RANGE) * SLOW_LEVEL # 目的地に近づいたらスピードを落とす
        
        # 中間地点に着いたら目的地を変更
        if self.middle and self.middle_position is not None:
            if np.linalg.norm(self.position - self.middle_position) < MIDDLE_RANGE:
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