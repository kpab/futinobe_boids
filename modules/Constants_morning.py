FRAME_COUNT = 6300
SKIP_RESULT_COUNT = 300 # 結果にカウントしないフレーム数
BORN_RATE = 0.8
FUTINOBE_RATE = 0.2 # 淵野辺率

MAX_SPEED = 2.5 # 🦵
MAX_MAX_SPEED = [3.0, 0.5] # 上振れ最高速度, 確率
MIN_MAX_SPEED = [2.0, 0.1] # 下振れ最高速度, 確率

START_HUMAN_COUNT = 10 # 初期

HITO_SIYA_LEVEL = 16.0 # 👁️
WALL_SIYA_LEVEL = 16.0 # 👁️

SEKKATI = 0.3
YASASISA = 0.08 # 人回避の重み
AVOID_WALL_WEIGHT = 0.1 # 壁回避の重み

MIDDLE_RANGE = 10 # 中間地点到達確認範囲
WIDTH = 500
HEIGHT = 500
WIDTH_HEATMAP = int(WIDTH/10)
HEIGHT_HEATMAP = int(HEIGHT/10)
now_frame = 0 # 現在のフレーム数

perfect_fake = False # やる
HIDE = True # 隠す

slowing_range = 30 # 減速範囲(ゴール-現在地<slowing_rangeで減速)
slow_level = 20

now_agents_positions = [[0 for j in range(WIDTH_HEATMAP)] for i in range(HEIGHT_HEATMAP)]