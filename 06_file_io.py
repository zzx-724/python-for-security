"""
Day 6: 文件读写 + JSON — 让脚本能读能存

为什么文件读写是必须的？

  回想你 Day 4、Day 5 写的扫描脚本，目标列表是【写死在代码里】的：

      targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

  问题来了：
    1. 想换一批目标扫 → 得改代码、重新运行，这不是工具，是"一次性脚本"
    2. 扫出来的结果 → print 在屏幕上，终端一关就没了，没法交差

  真正的工具是这样的：

      targets = load_targets("targets.txt")     # 从文件读目标
      results = scan(targets)                   # 扫描
      save_report(results, "report.json")       # 结果存成文件

  文件读写解决的就是这两件事：
    【数据不写死在代码里】 + 【结果留得住】

C 语言对比：

  C:      FILE *f = fopen("targets.txt", "r");
          // ...读写...
          fclose(f);              ← 容易忘！忘了就是资源泄漏

  Python: with open("targets.txt", "r", encoding="utf-8") as f:
              # ...读写...
          # 出了 with 块自动关闭，想忘都忘不掉

⚠️ 本文件运行会生成 targets.txt 和 scan_report.json。
   它们是【运行产物】不是源码 —— 已在 .gitignore 里排除，不会被 git 提交。
"""

import json


# ============================================================
# 一、打开文件的正确姿势：with open
# ============================================================
print("=" * 55)
print("  一、with open — 打开文件的正确姿势")
print("=" * 55)

# 一行代码里有三个东西，逐个拆开看：
#
#   with open("targets.txt", "w", encoding="utf-8") as f:
#   └┬─┘ └─┬┘ └─────┬─────┘  └┬┘ └───────┬───────┘    └┬┘
#    │    │      文件名      模式      编码           文件对象
#    │    └─ open() 是 Python 打开文件的内置函数
#    └─ with：出了这个代码块自动关闭文件（下面细讲）

# --- 为什么用 with？---
# 不用 with 的写法（能跑，但不推荐）：
#     f = open("a.txt", "w")
#     f.write("内容")
#     f.close()          ← 全靠你记得！
#
# 问题：如果 write 那行报错了，f.close() 永远不会执行，文件就一直被占用。
# with 相当于给文件加了个"自动门"：不管正常走还是中途出错，出去时都自动关上。

target_text = """# 目标列表（# 开头的是注释行，会被跳过）
192.168.1.1
192.168.1.2
192.168.1.3
10.0.0.1
"""

with open("targets.txt", "w", encoding="utf-8") as f:
    f.write(target_text)

print("[+] 已创建 targets.txt")
print("    现在去看一眼这个文件，它是真实存在于你磁盘上的")

# --- 为什么必须写 encoding="utf-8"？---
# 【在你的电脑上是刚需】刚才实测过：
#     你的系统默认编码是 cp936（GBK），不是 utf-8
#     不写 encoding 时，Python 用 GBK 存中文
#     换台机器（或换个软件）用 utf-8 去读 → 乱码 / 直接报错
#
# 一句话：encoding="utf-8" 是【跨平台保险】。
# 你不写，Windows 上一套编码、Linux 上另一套，代码就搬不了家。
#
# ⚠️ 铁律：open() 永远写 encoding="utf-8"，没有例外。


# ============================================================
# 二、写文件：w 和 a 两种模式
# ============================================================
print("\n" + "=" * 55)
print("  二、写文件：w 和 a")
print("=" * 55)

# 常用模式：
#   "w"  write   写入。⚠️ 会【清空原内容】再写！
#   "a"  append  追加。在原内容【末尾接着写】
#   "r"  read    读取（默认就是这个）

# --- 演示 "a" 追加 ---
with open("targets.txt", "a", encoding="utf-8") as f:
    f.write("172.16.0.1\n")            # 注意这里的 \n！不写就换不了行

print('[+] 用 "a" 模式追加了一行 172.16.0.1')
print("    文件现在应该有 5 个目标了")

# --- ⚠️ 警告："w" 会清空文件 ---
# 这一行如果放开，targets.txt 里的 5 个目标会全部消失，只剩这一行：
#     with open("targets.txt", "w", encoding="utf-8") as f:
#         f.write("只剩我了\n")
#
# 【这是新手最容易犯的数据丢失事故】——
# 你想"追加一行"，结果手一抖写了 "w"，整个文件被清空。
# 记住：想往后加内容，用 "a"，不是 "w"。


# ============================================================
# 三、读文件 —— 三种读法
# ============================================================
print("\n" + "=" * 55)
print("  三、读文件")
print("=" * 55)

# --- 读法 1：read() —— 一口气全读成一个字符串 ---
with open("targets.txt", "r", encoding="utf-8") as f:
    whole = f.read()
print("【read()】整个文件读成一个字符串:")
print(f"  {whole!r}")          # !r 表示"按原始样子显示"，能看到 \n

# --- 读法 2：readlines() —— 读成列表，每行一个元素 ---
with open("targets.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("\n【readlines()】读成列表:")
print(f"  {lines}")

# --- 读法 3：直接遍历（推荐）---
# 文件对象本身就能直接 for 循环，每次给你一行。
# 好处：不是一次性把整个文件读进内存，大文件也不会撑爆。
print("\n【直接遍历】一行一行处理（推荐，省内存）:")
with open("targets.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(f"  读到: {line!r}")

# ⚠️⚠️ 看到每行末尾那个 \n 了吗？这是必须理解的一步！
#   文件里每一行都带一个【换行符 \n】。
#   所以 line 的值是 "192.168.1.1\n"，不是 "192.168.1.1"。
#
#   这意味着：
#       "192.168.1.1\n" == "192.168.1.1"    →  False ！
#
#   拿这样的字符串去比较、去拼 URL、去当字典的 key，全都会错。
#
#   【Day 2 学的 strip() 在这里是刚需】：
#
#       line = line.strip()      # 去掉首尾空白（包括 \n 和空格）
#
#   处理文件读进来的每一行，第一件事永远先 strip()。

print("\n【strip() 之后】干净了:")
with open("targets.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean = line.strip()
        print(f"  {clean!r}")


# ============================================================
# 四、实战：load_targets() — 读目标列表
# ============================================================
print("\n" + "=" * 55)
print("  四、实战：load_targets()")
print("=" * 55)


def load_targets(filepath):
    """
    从文件加载目标列表

    规则：
      - 空行跳过
      - # 开头的行是注释，跳过
      - 其他行 strip() 之后当作一个目标
    返回：目标列表
    """
    targets = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()                    # 1. 先去掉 \n 和空格
            if line and not line.startswith("#"):  # 2. 非空 且 不是注释
                targets.append(line)               # 3. 收进列表
    return targets


targets = load_targets("targets.txt")
print(f"加载到 {len(targets)} 个目标: {targets}")

# 拆解那个 if 条件（这是文件读取里的万能模板）：
#     if line and not line.startswith("#"):
#        └┬─┘     └──────────┬──────────┘
#         │                  └─ 不是以 # 开头（Day 2 学的 startswith）
#         └─ line 非空。空字符串 "" 在 Python 里算 False
#
# 【为什么要有 "#" 这一条？】
#   现实中的目标文件常常长这样：
#       # 客户 A 的内网段
#       192.168.1.0/24
#       # 客户 B
#       10.0.0.0/24
#   注释让你能记住"这批目标是哪来的"，而程序自动跳过它们。
#   这是写工具的好习惯 —— 配置文件要能给人看。


# ============================================================
# 五、JSON — 把数据存成文件的标准格式
# ============================================================
print("\n" + "=" * 55)
print("  五、JSON")
print("=" * 55)

# 问题：扫描结果是【字典和列表的嵌套】，怎么存进文件？
#
#   坏办法：f.write(str(results))
#     存进去是 Python 的写法 {'a': 1}（单引号），别的语言读不了，
#     而且读回来还得用 eval() 解析 —— eval 是安全问题，永远别用。
#
#   好办法：JSON

# --- JSON 是什么？---
# 一种【纯文本的数据格式】，长得几乎和 Python 的字典一模一样：
#
#     Python                    JSON
#     {"ip": "10.0.0.1"}   ←→   {"ip": "10.0.0.1"}     双引号（JSON 只认双引号）
#     None                 ←→   null
#     True / False         ←→   true / false
#
# 【为什么用它】
#   1. 跨语言：Python 写的报告，JavaScript、Go、Java 都能直接读
#   2. 人能看懂（不像二进制）
#   3. Python 内置支持，字典直接存、直接读，不用自己拼字符串
#
# 安全工具的报告几乎都用 JSON —— 你的扫描结果最终要交给别的系统处理。

# --- 字典 → JSON 字符串（dumps = dump string）---
report = {
    "target": "192.168.1.1",
    "open_ports": [22, 80, 443],
    "os": "Linux",
}
json_text = json.dumps(report)
print("【json.dumps()】字典 → JSON 字符串:")
print(f"  {json_text}")

# --- 中文会变成 \uXXXX，加 ensure_ascii=False 解决 ---
report_cn = {"note": "扫描完成", "target": "192.168.1.1"}
print("\n默认（中文被转义成 \\uXXXX，人看不懂）:")
print(f"  {json.dumps(report_cn)}")
print("加 ensure_ascii=False（保留中文）:")
print(f"  {json.dumps(report_cn, ensure_ascii=False)}")

# --- indent=2 让格式好看（自动换行缩进）---
print("\n加 indent=2（格式化输出，人能读）:")
print(json.dumps(report, indent=2, ensure_ascii=False))

# 【记住这两个参数】写报告时永远带上：
#     ensure_ascii=False   中文不转义
#     indent=2             换行缩进，人能看懂


# ============================================================
# 六、实战：把报告存成文件 / 从文件读回来
# ============================================================
print("\n" + "=" * 55)
print("  六、实战：save_report / load_report")
print("=" * 55)


def save_report(results, filepath):
    """把扫描结果（列表/字典）保存成 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        #         ↑ 注意是 dump 不是 dumps！
        #           dump  = 直接写进文件对象
        #           dumps = 转成字符串（s = string）
    return filepath


def load_report(filepath):
    """从 JSON 文件读回数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        #      ↑ 同理：load 读文件，loads 读字符串
    return data


# 模拟一份扫描报告
scan_results = [
    {"ip": "192.168.1.1", "open_ports": [22, 80, 443], "os": "Linux"},
    {"ip": "192.168.1.2", "open_ports": [22, 3306], "os": "Linux"},
    {"ip": "192.168.1.3", "open_ports": [80], "os": "Windows"},
]

saved = save_report(scan_results, "scan_report.json")
print(f"[+] 报告已保存: {saved}")

# 读回来验证
loaded = load_report("scan_report.json")
print(f"[+] 读回来了，类型是 {type(loaded).__name__}，共 {len(loaded)} 条记录")
print(f"    第一条: {loaded[0]}")

# 关键验证：读回来的数据能【直接当字典用】
# 这才是 JSON 的价值 —— 不是一个死字符串，而是活的数据结构
print("\n读回来的数据照样能取值、能遍历:")
for record in loaded:
    ip = record["ip"]                       # 按 key 取值
    count = len(record["open_ports"])
    print(f"  {ip:<15} 开放 {count} 个端口")

# 【dumps/dump 和 loads/load 的区别，一次记牢】
#     带 s 的（dumps/loads）处理【字符串】  s = string
#     不带 s 的（dump/load） 处理【文件】    直接读写文件
#
#     存文件：  json.dump(数据, 文件对象)
#     读文件：  json.load(文件对象)
#
# 同理 Day 2 学过的 b64encode / b64decode 也是这个套路。


# ============================================================
# 七、练习（你来写）
# ============================================================
print("\n" + "=" * 55)
print("  七、练习")
print("=" * 55)

# ------------------------------------------------------------
# 练习 A：数一数文件有多少行
# ------------------------------------------------------------
# 任务：写一个函数 count_lines(filepath)，返回文件的行数（包括空行）
#
# 提示：
#   1. 用 with open(filepath, "r", encoding="utf-8") as f:
#   2. 准备一个计数器 count = 0
#   3. 遍历 f，每读一行 count += 1
#   4. return count
#
# 写完后测试：
#     print(count_lines("targets.txt"))

# === 你的代码写在这里 ===
def count_lines(filepath):
    '''返回文件的行数'''
    with open(filepath, "r", encoding="utf-8") as f:
        count = 0
        for line in f:
            print(f"读到: {line!r}")
            count += 1
        return count
print(count_lines("targets.txt"))

# ------------------------------------------------------------
# 练习 B：把列表存成文件（save_targets）
# ------------------------------------------------------------
# 场景：扫描完，你想把"存活主机"列表导出成 txt，每行一个。
#
# 任务：写一个函数 save_targets(targets, filepath)
#       把列表里的每个元素写成文件的一行
#
# 提示：
#   - 用 "w" 模式
#   - 遍历列表，每写一个元素后面要加 "\n"，否则全挤在一行
#   - ⚠️ f.write() 只能写【字符串】！如果元素是数字要先 str() 转换
#
# 写完后测试：
#     save_targets(["192.168.1.1", "192.168.1.2"], "alive.txt")
#     然后打开 alive.txt 看看内容对不对

# === 你的代码写在这里 ===
def save_targets(targets, filepath):
    '''把列表targets的每个元素写成文件的一行'''
    with open(filepath, "w", encoding="utf-8") as f:
        for target in targets:
            f.write(f"{target}\n")
save_targets(["192.168.1.1", "192.168.1.2"], "alive.txt")

# ------------------------------------------------------------
# 练习 C：修改 load_targets，统计跳过了几行
# ------------------------------------------------------------
# 任务：写一个函数 load_targets_verbose(filepath)
#       和 load_targets 一样加载目标，但【额外返回两个数】：
#         跳过了几行注释、跳过了几行空行
#
#       返回值格式：(目标列表, 注释行数, 空行数)
#
# 提示：
#   - 两个计数器：comment_count、blank_count
#   - 判断顺序很重要：
#         先 strip()，再判断是不是空行，再判断是不是注释
#   - 最后 return targets, comment_count, blank_count
#     （知道吗？return 后面用逗号可以一次返回多个值，其实是元组）
#
# 写完后测试：
#     result, comments, blanks = load_targets_verbose("targets.txt")
#     print(f"目标 {len(result)} 个，跳过注释 {comments} 行，空行 {blanks} 行")

# === 你的代码写在这里 ===
def load_targets_verbose(filepath):
    """加载目标，同时统计跳过了多少注释行和空行。
    返回 (目标列表, 注释行数, 空行数)。
    """
    targets = []
    comment_count = 0
    blank_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                blank_count += 1
            elif line.startswith("#"):
                comment_count += 1
            else:
                targets.append(line)
    return targets, comment_count, blank_count

result, comments, blanks = load_targets_verbose("targets.txt")
print(f"目标 {len(result)} 个，跳过注释 {comments} 行，空行 {blanks} 行")

# ------------------------------------------------------------
# 练习 D：完整的"读-处理-存"流程（今天的综合题）
# ------------------------------------------------------------
# 场景：你有一个目标文件，要读出来、加工一下、再存成 JSON 报告。
#
# 任务：
#   1. 用 load_targets() 读出 targets.txt 里的目标
#   2. 构造一份报告，格式是一个列表，每个元素长这样：
#          {"ip": "192.168.1.1", "alive": True, "ports": []}
#      （alive 你就随便定：IP 结尾是奇数就当 True，偶数当 False —— 模拟存活探测）
#   3. 用 save_report() 存成 "day6_report.json"
#   4. 再用 load_report() 读回来，打印一共几条记录
#
# 提示：
#   - 构造报告用列表推导式（Day 4 学的）会很简洁：
#         report = [{"ip": ip, ...} for ip in targets]
#   - 判断奇偶：int(ip.split(".")[-1]) % 2  —— 取最后一段数字，看余数
#
# 做完之后，打开 day6_report.json 看一眼，确认是格式漂亮的 JSON。

# === 你的代码写在这里 ===
targets_1 = load_targets("targets.txt")
report = [
    {
        "ip": ip,
        "alive": int(ip.split(".")[-1]) % 2 == 1,
        "ports": []
    }
    for ip in targets_1
]
save_report(report, "day6_report.json")
loaded = load_report("day6_report.json")
print(f"报告共 {len(loaded)} 条记录")


# ============================================================
# 参考答案（先自己写！写完再对照）
# ============================================================
# 练习 A
# def count_lines(filepath):
#     """返回文件的行数"""
#     count = 0
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             count += 1
#     return count
#
#
# print(count_lines("targets.txt"))
#
# 【要点】这里不用 strip() 也能数对，因为你只是数个数，不关心每行内容。
#   但如果要比较行内容，就一定要 strip。
#
# 练习 B
# def save_targets(targets, filepath):
#     """把列表写成文件，每行一个元素"""
#     with open(filepath, "w", encoding="utf-8") as f:
#         for item in targets:
#             f.write(f"{item}\n")        # 加 \n 才能换行
#     return filepath
#
#
# save_targets(["192.168.1.1", "192.168.1.2"], "alive.txt")
#
# 【要点】f"{item}\n" 比 str(item) + "\n" 更简洁，而且数字也能自动转字符串。
#   如果忘了 \n，所有内容会挤在一行：'192.168.1.1192.168.1.2'
#
# 练习 C
# def load_targets_verbose(filepath):
#     """加载目标，同时统计跳过了多少注释行和空行"""
#     targets = []
#     comment_count = 0
#     blank_count = 0
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line:                        # 空行
#                 blank_count += 1
#             elif line.startswith("#"):          # 注释行
#                 comment_count += 1
#             else:                               # 真正的目标
#                 targets.append(line)
#     return targets, comment_count, blank_count
#
#
# result, comments, blanks = load_targets_verbose("targets.txt")
# print(f"目标 {len(result)} 个，跳过注释 {comments} 行，空行 {blanks} 行")
#
# 【要点】注意判断顺序！必须先判断"是不是空行"再判断"是不是注释"。
#   因为对空行来说 line.startswith("#") 是 False，顺序反了会把空行算进"其他"。
#
# 练习 D
# targets = load_targets("targets.txt")
#
# report = []
# for ip in targets:
#     last = int(ip.split(".")[-1])       # 取 IP 最后一段，转成数字
#     alive = last % 2 == 1               # 奇数算存活
#     report.append({"ip": ip, "alive": alive, "ports": []})
#
# save_report(report, "day6_report.json")
# loaded = load_report("day6_report.json")
# print(f"报告共 {len(loaded)} 条记录")
#
# 【要点】ip.split(".")[-1] 是 Day 2 的 split + Day 3 的 [-1] 索引组合：
#   "192.168.1.1".split(".")  →  ['192', '168', '1', '1']
#   取 [-1] 就是最后一段 '1'，再 int() 变成数字 1。
#   这种"字符串 → 列表 → 取元素"的组合，是处理 IP、URL、路径的常用套路。
