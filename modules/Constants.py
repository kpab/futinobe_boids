FRAME_COUNT = 500
START_HUMAN_COUNT = 10 # 初期
HITO_SIYA_LEVEL = 16.0 # 👁️
WALL_SIYA_LEVEL = 16.0 # 👁️
MAX_SPEED = 3.0 # 🦵
BORN_RATE = 0.6
SEKKATI = 0.3
YASASISA = 0.08 # 人回避の重み
AVOID_WALL_WEIGHT = 0.1 # 壁回避の重み
FUTINOBE_RATE = 0.2 # 淵野辺率
MIDDLE_RANGE = 30 # 中間地点到達確認範囲

perfect_fake = False # やる


slowing_range = 50 # 減速範囲(ゴール-現在地<slowing_rangeで減速)
slow_level = 20