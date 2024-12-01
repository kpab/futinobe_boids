from modules.Constants_morning import *
import numpy as np
import matplotlib
if BACKGROUND:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from modules.Constants_morning import *
from modules.Agent import Agent
from modules.Result import *
from modules.GappingHeatmap import GappingHeatmap

import datetime

now_agents_positions = [[0 for j in range(WIDTH_HEATMAP)] for i in range(HEIGHT_HEATMAP)]
now_frame = 0 # 現在のフレーム数

class Simulation:
    def __init__(self, width, height, sim_name="no-name"):
        self.sim_name = sim_name
        self.width = width
        self.height = height
        self.agents = []
        self.walls = []
        self.fake_walls = []
        self.start_positions = []
        self.start_enter_position_weights = [] # スタート地点の確率を反映
        self.start_exit_position_weights = []
        self.start_enter = []
        self.start_exit = []
        self.start_middle = [] # 中間地点が必要なスタート位置
        self.start_middle_v2 = [] # 右階段利用淵野辺ワーカー
        self.goals = []
        self.goal_enter_position_weights = []
        self.goal_exit_position_weights = []
        self.middle_goals = [] # 中間地点が必要な目的地
        self.middle_goals_v2 = [] # 右階段利用淵野辺民
        self.middle_positions = [] # 中間地点(右)
        self.middle_positions_v2 = [] # 中間地点(左)
        self.goal_enter = []
        self.goal_exit = []
        self.colors = ['red', 'blue', 'green', 'pink', 'purple']
        self.goaled_agents = []


    # 壁
    def add_wall(self, x1, y1, x2, y2):
        self.walls.append((x1, y1, x2, y2))

    # フェイク壁
    def add_fake_wall(self, x1, y1, x2, y2):
        self.fake_walls.append((x1, y1, x2, y2))

   

    # スタート位置
    def add_start_position(self, x, y, weight, futinobe, middle=False, middle_2=False):
        self.start_positions.append((x, y))
        if futinobe:
            self.start_enter.append((x, y))
            for _ in range(weight):
                self.start_enter_position_weights.append((x, y))
        else:
            self.start_exit.append((x, y))
            for _ in range(weight):
                self.start_exit_position_weights.append((x, y))
        if middle:
            self.start_middle.append((x, y))
        if middle_2:
            self.start_middle_v2.append((x, y))

    # 目的地
    def add_goal(self, x, y, weight, futinobe, middle=False, middle_2=False):
        self.goals.append((x, y))
        if futinobe:
            self.goal_enter.append((x, y))
            for _ in range(weight):
                self.goal_enter_position_weights.append((x, y))
        else:
            self.goal_exit.append((x, y))
            for _ in range(weight):
                self.goal_exit_position_weights.append((x, y))
        if middle:
            self.middle_goals.append((x, y))
        if middle_2:
            self.middle_goals_v2.append((x, y))

    # 中間地点
    def add_middle_position(self, x, y, Right=False):
        if Right:
            self.middle_positions_v2.append((x, y))
        else:
            self.middle_positions.append((x, y))

    # エージェントの生成
    def born_agent(self):
        middle = False
        middle_position = None
        if not self.start_positions or not self.goals:
            return
        
        if np.random.rand() < FUTINOBE_RATE:
            futinobe = True
        else:
            futinobe = False
            
        if futinobe:
            start_position = self.start_enter_position_weights[np.random.randint(len(self.start_enter_position_weights))]
            goal = self.goal_enter_position_weights[np.random.randint(len(self.goal_enter_position_weights))]
            # -- 目的地が中間地点であるか、スタート位置が中間地点であるか --
            if goal in self.middle_goals or start_position in self.start_middle:
                middle = True
                middle_position = self.middle_positions[np.random.randint(len(self.middle_positions))]
            elif goal in self.middle_goals_v2 or start_position in self.start_middle_v2:
                middle = True
                middle_position = self.middle_positions_v2[np.random.randint(len(self.middle_positions_v2))]
        
            color = "blue"
        else:
            start_position = self.start_exit_position_weights[np.random.randint(len(self.start_exit_position_weights))]
            goal = self.goal_exit_position_weights[np.random.randint(len(self.goal_exit_position_weights))]
            # -- 目的地が中間地点であるか、スタート位置が中間地点であるか --
            if goal in self.middle_goals or start_position in self.start_middle:
                middle = True
                middle_position = self.middle_positions[np.random.randint(len(self.middle_positions))]
            elif goal in self.middle_goals_v2 or start_position in self.start_middle_v2:
                middle = True
                middle_position = self.middle_positions_v2[np.random.randint(len(self.middle_positions_v2))]

            color = "red"
        
        self.agents.append(Agent(start_position, goal, color, futinobe, middle, middle_position))

    def update(self):
        global now_frame

        if now_frame >= FRAME_COUNT:
            # sys.exit()
            
            return
        else:
            now_frame += 1
        # -- 現在地リスト格納 --
        if now_frame > SKIP_RESULT_COUNT:
            ChkAgentPos(now_agents_positions, self.agents)

        for agent in self.agents: # 位置こーしん
            agent.update(self.agents, self.walls)

        # -- 到着エージェントの削除 --
        for agent in self.agents:
            if np.linalg.norm(agent.position - agent.goal) < 15:
                self.agents.remove(agent)
                if now_frame > SKIP_RESULT_COUNT:
                    self.goaled_agents.append(agent)
                    continue
            if agent.futinobe:
                for g in self.goal_enter:
                    if np.linalg.norm(agent.position - g) < 15:
                        if agent in self.agents:
                            self.agents.remove(agent)
                        if now_frame > SKIP_RESULT_COUNT:
                            self.goaled_agents.append(agent)
                        continue
            else:
                for g in self.goal_exit:
                    if np.linalg.norm(agent.position - g) < 15:
                        if agent in self.agents:
                            self.agents.remove(agent)
                        if now_frame > SKIP_RESULT_COUNT:
                            self.goaled_agents.append(agent)
                        continue

        for _ in range(2):
            if np.random.rand() < BORN_RATE: # 生成
                self.born_agent()

    def animate(self, num_frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        text = ax.text(250, 520, 0, ha='center')
        
        # 壁の描画
        for wall in self.walls:
            ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1]))

        for wall in self.fake_walls:
            if PERFECT_FAKE:
                ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1]))
            else:
                ax.add_patch(Rectangle((wall[0], wall[1]), wall[2]-wall[0], wall[3]-wall[1],fc="r"))

        # 中間地点の描画
        if not PERFECT_FAKE:
            for middle in self.middle_positions:
                ax.plot(middle[0], middle[1], 'g*', markersize=10)
            for middle in self.middle_positions_v2:
                ax.plot(middle[0], middle[1], 'g*', markersize=10)

        # 目的地の描画
        for dest in self.goal_enter:
            ax.plot(dest[0], dest[1], 'b*', markersize=10)
        for dest in self.goal_exit:
            ax.plot(dest[0], dest[1], 'r*', markersize=10)

        # スタート位置の描画
        for start in self.start_enter:
            ax.plot(start[0], start[1], 'bo', markersize=5)
        for start in self.start_exit:
            ax.plot(start[0], start[1], 'ro', markersize=5)

        scatter = ax.scatter([], [], c=[])

        def update(frame):
            if now_frame %5000 == 0 and now_frame>SKIP_RESULT_COUNT:
                # print(now_frame)
                t_delta = datetime.timedelta(hours=9)
                JST = datetime.timezone(t_delta, 'JST')
                now = datetime.datetime.now(JST)
                d = now.strftime('%Y/%m/%d %I:%M(%p)')
                fig_name = now.strftime('%Y%m%d%H%M')
                with open(LOG_NAME, "a") as f:
                    f.write(f"ふる: {now_agents_positions}\n")
                Heatmapping(now_agents_positions, self.walls)
                HeatmappingNumber(now_agents_positions, self.walls, fig_name)
                SayResult(now_frame, self.goaled_agents)
                ChkTopFive(now_agents_positions)
                CalcStandardHensa(now_agents_positions, fig_name)
                HazuretiHako(now_agents_positions, fig_name)
            if now_frame == FRAME_COUNT:
                plt.close(fig)
                return []
            # print(np.array([agent.position for agent in self.agents]))
            self.update()
            if not HIDE:
                scatter.set_offsets([agent.position for agent in self.agents])
                scatter.set_color([agent.color for agent in self.agents])
            text.set_text(now_frame)
            
            return scatter,

        anim = FuncAnimation(fig, update, frames=num_frames, interval=50, blit=False)
        # ax.invert_yaxis()
        plt.show()
       
        # -- 結果の出力 --
        # -- 日付 --
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        d = now.strftime('%Y/%m/%d %I:%M(%p)')
        fig_name = now.strftime('%Y%m%d%H%M')

        with open(LOG_NAME, "a") as f:
            f.write("-------------------------------\n")
            f.write(f"記録: {d}\n")
            f.write(f"{self.sim_name}\n")
            f.write(f"全部: {now_agents_positions}\n") # 12/1追加

        Heatmapping(now_agents_positions, self.walls)
        HeatmappingNumber(now_agents_positions, self.walls, fig_name)
        SayResult(now_frame, self.goaled_agents)
        ChkTopFive(now_agents_positions)
        CalcStandardHensa(now_agents_positions, fig_name)
        HazuretiHako(now_agents_positions, fig_name)
        # GappingHeatmap()
        return []

