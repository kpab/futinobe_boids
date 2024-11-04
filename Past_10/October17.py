'''
レイアウトの変更
'''
from modules.Constants import *
from modules.Simulation import Simulation

# シミュレーションの設定
sim = Simulation(500, 500)

# 壁の追加
sim.add_wall(0, 0, 30, 500) # 左
# sim.add_wall(485, 0, 500, 500) # 右
sim.add_wall(480, 360, 500, 500) # 右
sim.add_wall(0, 450, 290, 500) # 上
sim.add_wall(290, 480, 500, 500) # 上
sim.add_wall(0, 0, 500, 150) # 下
sim.add_wall(0, 0, 300, 300) # 左下

sim.add_wall(250, 370, 290, 450)
sim.add_wall(240, 380, 250, 450)
sim.add_wall(230, 390, 250, 450)
sim.add_wall(220, 400, 230, 450)
sim.add_wall(210, 410, 220, 450)
sim.add_wall(200, 420, 210, 450)
sim.add_wall(190, 430, 200, 450)
sim.add_wall(50, 300, 150, 320)

# フェイク壁
# sim.add_fake_wall(475, 0, 500, 500)
sim.add_fake_wall(30,300, 50, 450)
sim.add_fake_wall(290, 370, 300, 450)
sim.add_fake_wall(290, 450, 500, 480) # 上

# スタート位置の追加
### add_start_position(x, y, weight, futinobe, middle, middle_2)
# --- futinobe person ---
sim.add_start_position(490, 200, 1, True, False)
sim.add_start_position(490, 220, 1, True, False)
sim.add_start_position(490, 240, 2, True, False)

# --- futinobe worker ---
# 階段(奥)
sim.add_start_position(55, 440, 1, False, True)
sim.add_start_position(55, 430, 1, False, True)
sim.add_start_position(55, 420, 1, False, True) 
sim.add_start_position(55, 410, 1, False, True)

# エスカレーター(上り)
sim.add_start_position(310, 440, 5, False) 
sim.add_start_position(310, 420, 5, False) 

# 階段(右)
sim.add_start_position(470, 440, 1, False, middle_2=True)
sim.add_start_position(470, 430, 1, False, middle_2=True)
sim.add_start_position(470, 420, 1, False, middle_2=True) 
sim.add_start_position(470, 410, 1, False, middle_2=True) 
sim.add_start_position(470, 400, 1, False, middle_2=True) 
sim.add_start_position(470, 390, 1, False, middle_2=True) 
sim.add_start_position(470, 380, 1, False, middle_2=True) 

# ------------------------------
### add_goal(x, y, weight, futinobe, middle, middle_2)
# 目的地(確率あり）
sim.add_goal(490, 260, 1, False)  # 40%の確率
sim.add_goal(490, 280, 1, False)
sim.add_goal(490, 300, 2, False)
sim.add_goal(490, 320, 2, False)

# 階段(右)
sim.add_goal(470, 440, 1, True, False, True)
sim.add_goal(470, 430, 1, True, False, True)
sim.add_goal(470, 420, 1, True, False, True)
sim.add_goal(470, 410, 1, True, False, True) 
sim.add_goal(470, 400, 1, True, False, True) 
sim.add_goal(470, 390, 1, True, False, True) 
sim.add_goal(470, 380, 1, True, False, True) 

# 階段(奥)
sim.add_goal(55, 400, 1, True, True) 
sim.add_goal(55, 390, 1, True, True)
sim.add_goal(55, 380, 1, True, True)
sim.add_goal(55, 370, 1, True, True)

# エスカレーター(下り)
sim.add_goal(310, 400, 1, True) 
sim.add_goal(310, 380, 1, True) 

# ------------------------------
# 中間地点
## add_middle_position(x, y, Right=False)
sim.add_middle_position(300, 310)
sim.add_middle_position(300, 320)
sim.add_middle_position(300, 330)
sim.add_middle_position(300, 340)
sim.add_middle_position(300, 350)
sim.add_middle_position(300, 360)

sim.add_middle_position(460, 370, True)
sim.add_middle_position(455, 370, True)
sim.add_middle_position(450, 370, True)
sim.add_middle_position(445, 370, True)
sim.add_middle_position(440, 370, True)
sim.add_middle_position(435, 370, True)
sim.add_middle_position(430, 370, True)
sim.add_middle_position(425, 370, True)


# 初期エージェントの生成
for _ in range(START_HUMAN_COUNT):
    sim.born_agent()

# アニメーションの実行
sim.animate(FRAME_COUNT)

