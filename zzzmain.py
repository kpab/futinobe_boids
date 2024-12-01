# メイン使用
import subprocess

normalpy = "./Nobember06.py"  # 相対パス
wall_1py = "./Nobember07.py"
a_1py = "./Nobember08.py"
wall_2py = "./Nobember09.py"
n = "./Dcember01.py"

# pys = [
#     wall_1py, 
#     wall_1py, 
#     wall_1py, 
#     wall_1py, 
#     wall_1py, 
#     a_1py, 
#     a_1py, 
#     a_1py, 
#     a_1py, 
#     a_1py
# ]

subprocess.run(["python3", n])

# for _ in range(8):
#     subprocess.run(["python3", wall_2py])

# for py in pys:
#     subprocess.run(["python3", py])


# 並列でやる時
# for py in pys:
#     doing = subprocess.Popen(["python3", py])
