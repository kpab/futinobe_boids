import math
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.patches import Rectangle
from modules.Constants import *

# エージェントの現在地取得
def ChkAgentPos(now_agents_positions, agents):
    for agent in agents:
        # print(agent.position)
        now_agents_positions[math.floor(agent.position[1])//10][math.floor(agent.position[0])//10] += 1
    
    return now_agents_positions


def Heatmapping(now_agents_positions, walls):
    print(now_agents_positions)
    fig, ax = plt.subplots(figsize=(10, 10),
                           facecolor="gainsboro")
    
    plt.gca().invert_yaxis() # こいつ効いてない
    
    ax.set_xlim(0, WIDTH_HEATMAP*2)
    ax.set_ylim(0, HEIGHT_HEATMAP)
    
    ax.set_title("全体ヒートマップ")
    sns.heatmap(now_agents_positions, cmap='Greens', square=True)
    for wall in walls:
            ax.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    plt.show()