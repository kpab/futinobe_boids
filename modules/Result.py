'''
11/4 平均速度の出力
11/13 最大人口密度出力
11/14 数値表示ヒートマップの追加
11/18 最大人口密度の座標取得
'''

import math
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.patches import Rectangle
from modules.Constants_morning import SKIP_RESULT_COUNT,WIDTH_HEATMAP,HEIGHT_HEATMAP
import numpy as np


# エージェントの現在地取得
def ChkAgentPos(now_agents_positions, agents):
    for agent in agents:
        # print(agent.position)
        now_agents_positions[math.floor(agent.position[1])//10][math.floor(agent.position[0])//10] += 1
    
    return now_agents_positions

def SayResult(frame, total_goaled_agents):
    agents_average_speed = 0
    print("frame: ",frame)
    if frame <=  SKIP_RESULT_COUNT:
        print("残念!!今回の結果は全てスキップされました")
        return
    if len(total_goaled_agents) < 1:
        print("まだ誰も着いてないよ。もう少し待とう")
        return
    futinobe_goaled_count = 0
    worker_goaled_count = 0
    print("ただいまのシミュレーション結果")
    print(f"フレーム数:{frame}\nスキップf:{SKIP_RESULT_COUNT}")
    for agent in total_goaled_agents:
        if agent.futinobe:
            futinobe_goaled_count += 1
        else:
            worker_goaled_count += 1
        agents_average_speed += agent.total_speed/agent.frame
    print(f"総脱出数: {len(total_goaled_agents)}人")
    print(f"脱出数/f: {round(len(total_goaled_agents)/(frame-SKIP_RESULT_COUNT+1), 3)}") # まるめてる
    print(f"平均速度: {round(agents_average_speed/len(total_goaled_agents), 3)}") # marumaru
    print(f"淵野辺民: {futinobe_goaled_count}\n淵野辺ワーカー: {worker_goaled_count}")
    if futinobe_goaled_count>worker_goaled_count:
        print("今回は淵野辺民の勝ちーーーー!!!")
    else:
        print("今回は淵野辺ワーカーの勝ちーーーー!!!")
             



# -- ヒートマップ --
def Heatmapping(now_agents_positions, walls):
    # print(now_agents_positions)
    
    fig, ax = plt.subplots(figsize=(10, 10),
                           facecolor="gainsboro")
    
    ax.set_xlim(0, WIDTH_HEATMAP)
    ax.set_ylim(0, HEIGHT_HEATMAP)
    # ax.set_ylim(HEIGHT_HEATMAP, 0) # こいつも
    
    ax.set_title("~ヒートマップ~")
    ax2 = sns.heatmap(now_agents_positions, cmap='Greens',cbar=False)
    for wall in walls:
            ax.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    ax2.invert_yaxis()
    plt.show()
    print(f"最大人口密度: {np.amax(now_agents_positions)}")
    now_agents_positions = np.array(now_agents_positions)
    max_point = np.unravel_index(np.argmax(now_agents_positions), now_agents_positions.shape)
    print([max_point[1], max_point[0]])

def HeatmappingNumber(now_agents_positions, walls):    
    fig, ax = plt.subplots(figsize=(10, 10),
                           facecolor="gainsboro")
    
    ax.set_xlim(0, WIDTH_HEATMAP)
    ax.set_ylim(0, HEIGHT_HEATMAP)

    ax.set_title("~ヒートマップ~")
    ax2 = sns.heatmap(now_agents_positions, cmap='Greens',cbar=False, annot=True, fmt='d', annot_kws={'fontsize':5})
    for wall in walls:
            ax.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    ax2.invert_yaxis()
    plt.show()

# 上位5%の通られたマスを出力
def ChkTopFive(now_agents_positions):
    # 二次元を一次元に変換
    now_agents_positions = sum(now_agents_positions, [])
    list.sort(now_agents_positions, reverse=True) # こうじゅん
    top_five = []
    for _ in range(4):
        top_five.append(now_agents_positions.pop(0))
    print("上位5: ", top_five)