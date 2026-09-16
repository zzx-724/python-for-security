"""
Day 1: Python 第一步 — 变量、类型、输入输出
安全场景：信息收集时处理用户输入、格式化输出扫描结果

运行方式：在 VS Code 里按 Ctrl+F5，或终端 python 01_first_steps.py
"""

# ============================================================
# 1. 变量 — Python 不需要声明类型！
# ============================================================
# C:  int port = 80;
#     char target[] = "192.168.1.1";
target_ip = "192.168.1.1"      # 目标 IP
port = 80                       # HTTP 端口
is_alive = True                 # 是否存活（首字母大写！）
response_time = 0.023           # 响应时间（秒）

# 打印变量
print("目标:", target_ip)
print("端口:", port)
print("存活:", is_alive)
print("响应:", response_time, "秒")

# ============================================================
# 2. 类型 — Python 自动判断，可以随时看类型
# ============================================================
print("\n--- 看看这些变量的类型 ---")
print(type(target_ip))     # <class 'str'>
print(type(port))          # <class 'int'>
print(type(is_alive))      # <class 'bool'>
print(type(response_time)) # <class 'float'>

# ============================================================
# 3. 输入 — input() 永远返回字符串
# ============================================================
print("\n--- 信息收集脚本模拟 ---")
target = input("请输入目标 IP 或域名: ")
port_str = input("请输入端口号（默认 80）: ")

# input 返回的是字符串！做数学运算要转换
port_num = int(port_str) if port_str else 80  # 如果留空，默认 80
print(f"\n[*] 开始扫描 {target}:{port_num} ...")

# ============================================================
# 4. f-string — 安全脚本中最常用的格式化方式
# ============================================================
# C: printf("Target: %s:%d\n", target, port);
# Python: 直接 f-string，变量塞进花括号

banner = "Apache/2.4.41"
status_code = 200

# 模拟扫描结果输出
print(f"[+] {target}:{port_num} 开放")
print(f"    Status: {status_code}")
print(f"    Server: {banner}")

# 十六进制、二进制格式化 — 密码学方向很常用
byte_val = 0x41  # 十六进制 A
print(f"\n十六进制 0x41 = 十进制 {byte_val} = 字符 {chr(byte_val)}")
print(f"255 的十六进制: {hex(255)}")
print(f"255 的二进制:   {bin(255)}")

# ============================================================
# 5. 练习：自己动手改
# ============================================================
# 试试：修改 target_ip、port，添加一个 scan_type 变量（"TCP"或"UDP"），
# 然后用 f-string 打印一句完整的扫描信息。
# 例如：print(f"扫描类型: {scan_type}, 目标: {target_ip}:{port}")

print("\n--- 练习区域 ---")
# 在这里写你的代码：
scan_type = "TCP"
print(f"[*] 扫描类型: {scan_type}, 目标: {target_ip}:{port}")
