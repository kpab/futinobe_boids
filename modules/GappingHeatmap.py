'''
12/1 作成
'''
import seaborn as sns
from modules.Constants_morning import WIDTH_HEATMAP, HEIGHT_HEATMAP

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np

normal_result = [[]] # 通常の踏まれた地点の二次元リスト

# ヒートマップの差の出力
def GappingHeatmap(now_agents_positions, walls, fig_name):    
    normal_result = np.array(normal_result)
    now_agents_positions = np.array(now_agents_positions)
    
    gap = now_agents_positions - normal_result

    fig2, ax2 = plt.subplots(figsize=(16, 10),
                           facecolor="gainsboro")
    
    ax2.set_xlim(0, WIDTH_HEATMAP)
    ax2.set_ylim(0, HEIGHT_HEATMAP)

    ax2.set_title("~ヒートマップ~")
    ax2 = sns.heatmap(gap, cmap='bwr',cbar=False, annot=True, fmt='d', annot_kws={'fontsize':5})
    for wall in walls:
            ax2.add_patch(Rectangle((wall[0]/10, wall[1]/10), (wall[2]-wall[0])/10, (wall[3]-wall[1])/10))
    ax2.invert_yaxis()
    # plt.show()
    fig2.savefig(f"z{fig_name}_gap.png")


# 箱ひげ図
