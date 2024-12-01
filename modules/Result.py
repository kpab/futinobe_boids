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
from modules.Constants_morning import SKIP_RESULT_COUNT,WIDTH_HEATMAP,HEIGHT_HEATMAP, LOG_NAME
import numpy as np

# エージェントの現在地取得
def ChkAgentPos(now_agents_positions, agents):
    for agent in agents:
        # サイズ変換
        x_index = int(math.floor(agent.position[0]) // 10) 
        y_index = int(math.floor(agent.position[1]) // 10)
        # 範囲制限
        x_index = np.clip(x_index, 0, WIDTH_HEATMAP - 1)
        y_index = np.clip(y_index, 0, HEIGHT_HEATMAP - 1)

        now_agents_positions[y_index][x_index] += 1
    
    return now_agents_positions

def SayResult(frame, total_goaled_agents):
    result = [] # ログファイル用
    agents_average_speed = 0
    print("frame: ",frame)
    if frame <=  SKIP_RESULT_COUNT:
        print("残念!!今回の結果は全てスキップされました")
        with open(LOG_NAME, "a") as f:
            print("残念!!今回の結果は全てスキップされました", file=f)
        return
    if len(total_goaled_agents) < 1:
        print("まだ誰も着いてないよ。もう少し待とう")
        with open(LOG_NAME, "a") as f:
            print("まだ誰も着いてないよ。もう少し待とう", file=f)
        return
    futinobe_goaled_count = 0
    worker_goaled_count = 0
    print("ただいまのシミュレーション結果")
    print(f"フレーム数:{frame}\nスキップf:{SKIP_RESULT_COUNT}")
    result.append(f"フレーム数:{frame}\nスキップf:{SKIP_RESULT_COUNT}")
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
    result.append(f"総脱出数: {len(total_goaled_agents)}人")
    result.append(f"脱出数/f: {round(len(total_goaled_agents)/(frame-SKIP_RESULT_COUNT+1), 3)}")
    result.append(f"平均速度: {round(agents_average_speed/len(total_goaled_agents), 3)}")
    result.append(f"淵野辺民: {futinobe_goaled_count}\n淵野辺ワーカー: {worker_goaled_count}")
    if futinobe_goaled_count>worker_goaled_count:
        print("今回は淵野辺民の勝ちーーーー!!!")
    else:
        print("今回は淵野辺ワーカーの勝ちーーーー!!!")

    with open(LOG_NAME, "a") as f:
        for line in result:
            print(line, file=f)
             


# -- ヒートマップ --
def Heatmapping(now_agents_positions, walls):
    result = []
    fig, ax = plt.subplots(figsize=(10, 10),
                           facecolor="gainsboro")
    ax.set_xlim(0, WIDTH_HEATMAP)
    ax.set_ylim(0, HEIGHT_HEATMAP)
    
    ax.set_title("~ヒートマップ~")
    ax = sns.heatmap(now_agents_positions, cmap='Greens',cbar=False)
    for wall in walls:
            ax.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    ax.invert_yaxis()
    # plt.show()
    result.append(f"最大通過人数: {np.amax(now_agents_positions)}")
    print(f"最大通過人数: {np.amax(now_agents_positions)}")
    now_agents_positions = np.array(now_agents_positions)
    max_point = np.unravel_index(np.argmax(now_agents_positions), now_agents_positions.shape)
    result.append(f"最大通過地点: {[max_point[1], max_point[0]]}")
    print([max_point[1], max_point[0]])
    with open(LOG_NAME, "a") as f:
        for line in result:
            print(line, file=f)

def HeatmappingNumber(now_agents_positions, walls, fig_name):    
    fig2, ax2 = plt.subplots(figsize=(16, 10),
                           facecolor="gainsboro")
    
    ax2.set_xlim(0, WIDTH_HEATMAP)
    ax2.set_ylim(0, HEIGHT_HEATMAP)

    ax2.set_title("~ヒートマップ~")
    ax2 = sns.heatmap(now_agents_positions, cmap='Greens',cbar=False, annot=True, fmt='d', annot_kws={'fontsize':5})
    for wall in walls:
            ax2.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    ax2.invert_yaxis()
    # plt.show()
    fig2.savefig(f"z{fig_name}.png")

# 上位5位の通られたマスを出力→top20に変更します
def ChkTopFive(now_agents_positions):
    # 二次元を一次元に変換
    now_agents_positions = sum(now_agents_positions, [])
    list.sort(now_agents_positions, reverse=True) # こうじゅん
    top_five = []
    for _ in range(20):
        top_five.append(now_agents_positions.pop(0))
    # print("上位20: ", top_five)
    with open(LOG_NAME, "a") as f:
        print(f"上位20: {top_five}", file=f)
    

# 統計
def CalcStandardHensa(now_agents_positions, fig_name):
    # 二次元を一次元に変換
    now_agents_positions = sum(now_agents_positions, [])
    # 0を除去
    now_agents_positions = list(filter(lambda x: x!=0, now_agents_positions))
    now_agents_positions = np.array(now_agents_positions) # numpy配列に変換

    d1 = np.percentile(now_agents_positions, 25)
    d2 = np.percentile(now_agents_positions, 50)
    d3 = np.percentile(now_agents_positions, 75)

    # 箱ひげ図のプロット
    fig3, ax = plt.subplots()
    ax.boxplot(now_agents_positions, whis=[0, 100],vert=False, showmeans=True)  # 横向き, 外れ値表記しないver
    ax.set_title('箱ひげ図')
    ax.set_xlabel('通過人数')
    
    fig3.savefig(f"z{fig_name}_hako.png")

    std = np.std(now_agents_positions)
    print("標準偏差: ", std)
    with open(LOG_NAME, "a") as f:
        f.write(f"第一四分位数: {d1}\n")
        f.write(f"第二四分位数: {d2}\n")
        f.write(f"第三四分位数: {d3}\n")
        f.write(f"標準偏差: {round(std, 3)}\n")
        f.write("-------------------------------\n")


def HazuretiHako(now_agents_positions, fig_name):
    # 二次元を一次元に変換
    now_agents_positions = sum(now_agents_positions, [])
    # 0を除去
    now_agents_positions = list(filter(lambda x: x!=0, now_agents_positions))
    now_agents_positions = np.array(now_agents_positions) # numpy配列に変換

    # 箱ひげ図のプロット
    fig4, ax = plt.subplots()
    ax.boxplot(now_agents_positions, vert=False, showmeans=True, whis=1.2)  # 横向き, 外れ値表記しないver
    ax.set_title('箱ひげ図(外れ値あり)')
    ax.set_xlabel('通過人数')

    fig4.savefig(f"z{fig_name}_hakohazure.png")