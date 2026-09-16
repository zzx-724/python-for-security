"""
Day 4: 条件判断与循环 — 扫描逻辑的核心
安全场景：遍历 IP/端口、条件判断存活、过滤结果

Python 的 if/for/while 和 C 的 if/for/while 本质一样，
但 Python 写起来更简洁。
"""

import time
import random

# ============================================================
# 1. 条件判断 — 根据扫描结果做不同处理
# ============================================================

# C: if (status == 200) { printf("OK\n"); }
# Python: 不需要括号和大括号，靠缩进！

status = 200

if status == 200:
    print("[+] 200 OK — 页面存在")
elif status == 301 or status == 302:
    print("[~] 301/302 — 页面重定向")
elif status == 403:
    print("[!] 403 Forbidden — 存在但拒绝访问")
elif status == 404:
    print("[-] 404 Not Found — 页面不存在")
elif status == 500:
    print("[!] 500 — 服务器内部错误，可能有注入点")
else:
    print(f"[?] 未知状态码: {status}")

# Python 特有：in 运算符比一堆 || 简洁
# C: if (c == '/' || c == '.' || c == '\\' || c == '?') ...
# Python:
bad_chars = ['/', '.', '\\', '?', '%', '#', '&']
char = '/'
if char in bad_chars:
    print(f"'{char}' 是特殊字符，需要编码")

# ============================================================
# 2. for 循环 — 扫描遍历的主力
# ============================================================

targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
ports = [22, 80, 443]

print("\n--- 模拟端口扫描 ---")
# C: for (int i = 0; i < num_targets; i++) { for (int j = 0; j < num_ports; j++) { ... } }
# Python: 直接遍历，不需要管索引
for ip in targets:
    for port in ports:
        # 模拟扫描（用随机数模拟端口开闭）
        time.sleep(0.1)  # 模拟网络延迟
        is_open = random.choice([True, False, False, False])  # 25% 概率开放
        status_icon = "OPEN" if is_open else "closed"
        if is_open:
            print(f"  [+] {ip}:{port} - {status_icon}")

# Python 特有：enumerate 同时获取索引和值
print("\n带序号的端口列表:")
for i, port in enumerate(ports, 1):  # 从 1 开始计数
    print(f"  {i}. Port {port}")

# Python 特有：zip 并行遍历
print("\n主端口和备用端口:")
main_ports = [80, 443, 22]
backup_ports = [8080, 8443, 2222]
for main, backup in zip(main_ports, backup_ports):
    print(f"  主: {main} ← → 备用: {backup}")

# ============================================================
# 3. 列表/字典推导式 — Python 最强大的语法糖
# ============================================================

# C 写法（5-8 行）：过滤出 Web 端口
#  int web_ports[100]; int count=0;
#  for(int i=0; i<len; i++) { if(is_web(ports[i])) web_ports[count++]=ports[i]; }

# Python 写法（1 行）：
all_ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]
web_ports = [p for p in all_ports if p in {80, 443, 8080, 8443}]
print(f"\nWeb 端口过滤: {web_ports}")

# 带转换的推导式 — 生成 HTTP URL 列表
urls = [f"http://{ip}:{port}" for ip in targets for port in [80, 8080]]
print(f"待扫描 URL: {urls}")

# 字典推导式 — 端口状态表
status_table = {p: "closed" for p in ports}
status_table[80] = "open"  # 80 端口模拟开放
print(f"端口状态: {status_table}")

# ============================================================
# 4. 练习：批量存活探测
# ============================================================
print("\n--- 练习: 存活探测 ---")

# 目标列表 + 模拟扫描
scan_targets = [f"192.168.1.{i}" for i in range(1, 11)]  # 10 个 IP
alive_hosts = []  # 存活的 IP
dead_hosts = []   # 不存活的 IP

for ip in scan_targets:
    # 模拟 ping（随机 30% 存活率）
    is_alive = random.random() < 0.3
    if is_alive:
        alive_hosts.append(ip)
        print(f"  [ALIVE] {ip}")
    else:
        dead_hosts.append(ip)

print(f"\n存活: {len(alive_hosts)} 台, 离线: {len(dead_hosts)} 台")
print(f"存活列表: {alive_hosts}")

# 练习：用列表推导式改写上面的循环，直接从 scan_targets 过滤出存活主机
# 提示：先写一个 is_host_alive(ip) 函数，然后用 [ip for ip in scan_targets if is_host_alive(ip)]
