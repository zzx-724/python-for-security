"""
Day 3: 列表、字典、集合 — 安全数据的容器
安全场景：存端口列表、IP段、服务映射、目标去重

C 语言对比：
  C:      int ports[100];  int n = 0;   // 手动管理长度，满了要 realloc
  Python: ports = []       ports.append(80)   // 自动扩容，随便增删

C 里要手动数长度、手动扩容；Python 的列表/字典全自动，这是它写脚本快的原因。
"""

# ============================================================
# 一、列表 list — "一排有编号的格子"
# ============================================================
print("=" * 45)
print("  一、列表 list")
print("=" * 45)

# --- 创建：用方括号 []，逗号隔开 ---
common_ports = [21, 22, 23, 25, 53, 80, 443, 445, 3306, 3389, 8080]
print(f"端口列表: {common_ports}")
print(f"一共 {len(common_ports)} 个端口")   # len() = 长度，相当于 C 的 count

# --- 索引取值：和字符串完全一样，从 0 开始 ---
print(f"\n第 1 个端口 (索引0): {common_ports[0]}")     # 21
print(f"第 3 个端口 (索引2): {common_ports[2]}")       # 23
print(f"最后 1 个端口 (-1):  {common_ports[-1]}")      # 8080 ← -1 表示倒数第一！

# --- 切片：和字符串规则一样，含头不含尾 ---
print(f"\n前 3 个:      {common_ports[:3]}")      # [21, 22, 23]
print(f"第 4 个往后:  {common_ports[3:]}")        # [25, 53, ...]
print(f"倒数 3 个:    {common_ports[-3:]}")       # [3306, 3389, 8080]

# --- in 判断元素在不在里面（比写一堆 == 简洁）---
print(f"\n80 在列表里吗?   {80 in common_ports}")      # True
print(f"9999 在列表里吗? {9999 in common_ports}")      # False

# --- 增删改 ---
print("\n--- 增删改 ---")
common_ports.append(9090)        # 末尾追加
print(f"append(9090) 后: {common_ports}")

common_ports.insert(0, 7)        # 在索引 0 位置插入（原来的都往后挤）
print(f"insert(0, 7) 后: {common_ports}")

common_ports.remove(445)         # 按【值】删除 ⚠️ 值不存在会报错
print(f"remove(445) 后:  {common_ports}")

last = common_ports.pop()        # 删掉最后一个，并把它【返回】出来
print(f"pop() 删掉了:    {last}")
print(f"现在剩:          {common_ports}")

common_ports[0] = 9999           # 按【索引】直接改
print(f"ports[0]=9999 后: {common_ports}")

# --- 排序 ---
common_ports.sort()              # 从小到大排序（原地排序，直接改变自己）
print(f"\nsort() 排序后:   {common_ports}")

# --- 两个列表相加/相乘（Python 特色）---
print(f"\n列表相加 [1,2]+[3,4] = {[1, 2] + [3, 4]}")     # 拼接成一个
print(f"列表乘3  [0]*3       = {[0] * 3}")              # 重复3次 → [0,0,0]


# ============================================================
# 二、元组 tuple — "创建后就改不了的列表"
# ============================================================
print("\n" + "=" * 45)
print("  二、元组 tuple")
print("=" * 45)

# 用圆括号 () 创建。和列表的区别：不能增删改！
target = ("192.168.1.1", 80, "HTTP")
print(f"元组: {target}")
print(f"第 1 项: {target[0]}")      # 索引/切片和列表一样
print(f"后 2 项: {target[1:]}")

# target[0] = "1.1.1.1"    # ❌ 取消注释会报错！元组不可修改

# 为什么要有元组？
# 当你有一组"不该被改动的固定数据"时用它，表示"这是常量，别动"
# 比如：一个扫描目标的 IP/端口/协议，是绑死的三条信息，不该单独改其中一个

# 元组不可变 = 更安全。别人接手你的代码，看到元组就知道"这数据不会被改"


# ============================================================
# 三、字典 dict — "像查字典一样的键值对"
# ============================================================
print("\n" + "=" * 45)
print("  三、字典 dict")
print("=" * 45)

# 用花括号 {}，格式是 键: 值
# 安全场景：端口号 → 服务名，这天然就是"查表"关系
services = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
}
print(f"服务字典: {services}")

# --- 用 key 取值 ---
print(f"\n端口 80 的服务: {services[80]}")      # HTTP
print(f"端口 22 的服务: {services[22]}")        # SSH

# ⚠️ 大坑：取不存在的 key 会直接崩溃
# print(services[9999])    # ❌ KeyError: 9999  →  整个脚本挂掉

# ✅ 用 .get() 安全取值：取不到就返回你给的默认值
print(f"端口 9999 的服务: {services.get(9999, '未知服务')}")   # 未知服务
print(f"端口 80 的服务:   {services.get(80, '未知服务')}")     # HTTP

# 安全脚本里【永远用 .get()】，因为你不知道目标会返回什么

# --- 增 / 改：都是直接赋值，看 key 存不存在 ---
services[8080] = "HTTP-Proxy"    # key 不存在 → 新增
services[80] = "WEB"             # key 已存在 → 覆盖修改
print(f"\n增改之后: {services}")

# --- 删 ---
del services[21]                 # 删掉 key 为 21 的项
print(f"删掉 21 之后: {services}")

# --- 查 ---
print(f"\n3306 是 key 吗? {3306 in services}")    # True（判断 key，不是 value！）
print(f"字典里有几项:   {len(services)}")
print(f"所有 key:       {list(services.keys())}")
print(f"所有 value:     {list(services.values())}")


# ============================================================
# 四、集合 set — "自动去重的袋子"
# ============================================================
print("\n" + "=" * 45)
print("  四、集合 set")
print("=" * 45)

# 安全场景：从多个来源收集 IP，重复的一大堆，集合自动帮你去掉
source1 = ["192.168.1.1", "192.168.1.2", "192.168.1.1", "192.168.1.2"]   # 很多重复
source2 = ["192.168.1.2", "192.168.1.3", "192.168.1.4"]

print(f"原始 source1 (4个): {source1}")
print(f"转成集合后:         {set(source1)}")     # 只剩 2 个，自动去重！

# --- 三种集合运算 ---
# | 并集：两边所有的（去重）
print(f"\n并集 (|) 全部目标: {set(source1) | set(source2)}")

# & 交集：两边都有的
print(f"交集 (&) 都有:     {set(source1) & set(source2)}")

# - 差集：左边有、右边没有的
print(f"差集 (-) 仅源1有:  {set(source1) - set(source2)}")

# ⚠️ 集合是无序的！每次运行打印顺序可能不同，不要依赖顺序
# ✅ 需要有序就转回列表：sorted(set(source1))


# ============================================================
# 五、练习（你来写）
# ============================================================
print("\n" + "=" * 45)
print("  五、练习")
print("=" * 45)

# ------------------------------------------------------------
# 练习 A：列表操作
# ------------------------------------------------------------
ports = [22, 80, 443, 3306, 8080]

# 任务：
#   1. 在末尾追加 9000
#   2. 用 pop() 取出最后一个并打印出来
#   3. 打印"一共有几个端口"（用 len）
#   4. 判断 3306 在不在列表里，打印 True/False
#   5. 打印前 3 个端口

# === 你的代码写在这里 ===
ports.append(9000)
print(f"增加后的ports: {ports}")

print(f"最后一个: {ports.pop()}")
print(f"pop后的ports: {ports}")

print(f"一共有{len(ports)}个端口")

print(f"3306 在不在列表里? {3306 in ports}")

print(f"前3个端口: {ports[:3]}")

# ------------------------------------------------------------
# 练习 B：字典（端口 → 服务）
# ------------------------------------------------------------
# 任务：
#   1. 建一个字典 service_map，包含：21→FTP, 22→SSH, 3306→MySQL, 3389→RDP
#   2. 打印 22 对应的服务
#   3. 用 .get() 查询 9999，取不到时显示 "未知"
#   4. 新增一项 8080 → "HTTP-Proxy"
#   5. 把 21 的服务改成 "FTP(明文传输)"
#   6. 打印整个字典看看

# === 你的代码写在这里 ===
service_map = {
    21:"FTP",
    22:"SSH",
    3306:"MySQL",
    3389:"RDP",
}
print(f"\n新建字典: {service_map}")
print(f"22对应的服务: {service_map[22]}")
print(f"查询9999: {service_map.get(9999,'未知')}")
service_map[8080] = "HTTP-Proxy"
print(f"新增后的字典: {service_map}")
service_map[21] = "FTP(明文传输)"
print(f"修改后的字典: {service_map}")

# ------------------------------------------------------------
# 练习 C：集合去重（两个扫描器结果合并）
# ------------------------------------------------------------
scanner_a = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.2"]
scanner_b = ["10.0.0.3", "10.0.0.4", "10.0.0.1"]

# 任务：
#   1. 两个扫描器加起来，一共扫到哪些【不重复】的 IP？打印出来
#   2. 两个扫描器【都】扫到的 IP 是哪些？打印出来
#   3. 只有 scanner_a 扫到、scanner_b 没扫到的 IP 是哪些？

# === 你的代码写在这里 ===
print(f"\n加起来不重复的IP: {set(scanner_a) | set(scanner_b)}")
print(f"都扫到的IP: {set(scanner_a) & set(scanner_b)}")
print(f"只有 scanner_a 扫到、scanner_b 没扫到的 IP: {set(scanner_a) - set(scanner_b)}")

# ============================================================
# ⛔ 以下内容超纲，Day 4 / Day 5 再回来看
# ============================================================
# 列表推导式 → Day 4 学
#   web_ports = [p for p in ports if p in [80, 443]]
#
# for 循环遍历 → Day 4 学
#   for ip, ports in scan_result.items():
#       print(f"{ip} 开放端口: {ports}")
#
# 函数 def → Day 5 学
#   def generate_ips(subnet, start, end):
#       return [f"{subnet}.{i}" for i in range(start, end + 1)]
