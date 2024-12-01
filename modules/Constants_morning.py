# 朝ラッシュ用定数
# ------------------------
FRAME_COUNT = 50300
SKIP_RESULT_COUNT = 300 # 結果にカウントしないフレーム数
BORN_RATE = 0.8
FUTINOBE_RATE = 0.2 # 淵野辺率

MAX_SPEED = 2.5 # 🦵
MAX_MAX_SPEED = [3.0, 0.5] # 上振れ最高速度, 確率
MIN_MAX_SPEED = [2.0, 0.1] # 下振れ最高速度, 確率

# -------------------------

START_HUMAN_COUNT = 10 # 初期（skipするけどね）

# -- エージェント能力系定数(固定) --
HITO_SIYA_LEVEL = 16.0 # 👁️
WALL_SIYA_LEVEL = 16.0 # 👁️
SEKKATI = 0.3
YASASISA = 0.08 # 人回避の重み
AVOID_WALL_WEIGHT = 0.1 # 壁回避の重み
MIDDLE_RANGE = 10 # 中間地点到達確認範囲
SLOWING_RANGE = 30 # 減速範囲(ゴール-現在地<SLOWING_RANGEで減速)
SLOW_LEVEL = 20
# -- マップ系定数 --
WIDTH = 500
HEIGHT = 500
WIDTH_HEATMAP = int(WIDTH/10)
HEIGHT_HEATMAP = int(HEIGHT/10)

# 壁置く時:全部False
# シミュレーション回す時、全部True

PERFECT_FAKE = True # やる
HIDE = True # シミュレーション隠すか
BACKGROUND = True # Backgroundか
# ----------------
LOG_NAME = "zylog.txt"
