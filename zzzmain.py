# メイン使用
import subprocess

normalpy = "./Nobember06.py"  # 相対パス
wall_1py = "./Nobember07.py"
a_1py = "./Nobember08.py"

pys = [
    normalpy, 
    normalpy, 
    normalpy, 
    wall_1py, 
    wall_1py, 
    wall_1py, 
    a_1py, 
    a_1py, 
    a_1py
    ]


for py in pys:
    subprocess.run(["python3", py])


# 並列でやる時
# for py in pys:
#     doing = subprocess.Popen(["python3", py])
