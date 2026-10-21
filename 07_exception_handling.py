"""
Day 7: 异常处理 — 让程序在脏数据里活下来

为什么这一课比学新语法更重要？

  你昨天写的 project_01_log_analyzer.py，在 46 行干净的日志上跑得很好。
  但真实的 access.log 里，一定会有坏行：

      - 被截断的行（服务器写盘时断电）
      - 空行（某种中间件插入的）
      - 格式不对的行（别的程序写进了同一个文件）
      - 编码错误的字节

  遇到这些，你的 parts[6] 会直接抛 IndexError，
  然后【整个程序停在第 7 行】，剩下几十万行一行都不会再处理。

  安全和运维工具的第一要求，不是"快"，是：
      【不能因为一条脏数据就停工。】

  这就是异常处理存在的唯一理由。

C 语言对比：

  C:      没有异常机制，全靠返回值判断
          FILE *fp = fopen("x.txt", "r");
          if (fp == NULL) { perror("open"); return -1; }     ← 必须手动检查

          if (fgets(buf, sizeof buf, fp) == NULL) { ... }     ← 又一个

          每个可能失败的地方都要写一行检查，漏一个就崩。
          而且"正常逻辑"和"错误处理"混在一起，读起来很累。

  Python: try / except
          把【正常流程】和【出错了怎么办】分成两块写，主逻辑保持干净。

⚠️ 本文件会生成 bad_access.log（练习用），它是运行产物，已被 .gitignore 排除。
"""

from pathlib import Path


# ============================================================
# 一、先看崩溃 —— 用你昨天项目里的那行代码
# ============================================================
print("=" * 55)
print("  一、先看崩溃")
print("=" * 55)

# 模拟一个真实的日志文件：3 行正常 + 2 行坏的
log_lines = [
    '192.168.1.50 - - [13/Oct/2026:09:15:38 +0800] "GET /index.html HTTP/1.1" 200 2111',
    '10.0.0.99 - - [13/Oct/2026:02:24:23 +0800] "GET /admin/login HTTP/1.1" 404 330',
    '',                                                                    # 空行
    '203.0.113.7 - - [13/Oct/2026:03:01:39 +0800] "GET /.env HTTP/1.1" 403 452',
    '192.168.1.77 - - [13/Oct/2026',                                       # 被截断的行
]

# ---- 如果直接跑下面这段，会发生什么？----
#
#     for line in log_lines:
#         parts = line.split()
#         print(parts[6])
#
# 第 1、2 行正常。
# 第 3 行（空行）：line.split() 得到 []，parts[6] → IndexError
#
#     Traceback (most recent call last):
#       File "xxx.py", line 3, in <module>
#         print(parts[6])
#     IndexError: list index out of range
#
# 【重点】注意程序停在哪里 —— 第 3 行。
# 后面的第 4、5 行，永远不会被处理。
# 一条坏数据 = 丢掉后面所有的数据。这是最不能接受的失败方式。


# ---- 加上 try / except 之后 ----
print("\n加防护之后：")
good = 0
bad = 0

for line in log_lines:
    try:
        parts = line.split()
        path = parts[6]
        print(f"  [+] {parts[0]:<15} {path}")
        good += 1
    except IndexError:
        # 只有【这一行】被跳过，循环继续往下跑
        print(f"  [!] 跳过坏行: {line!r}")
        bad += 1

print(f"\n  正常 {good} 行，跳过 {bad} 行")
print("  ↑ 程序活下来了。坏行被记录下来，但没有拖垮整个流程。")


# ============================================================
# 二、try / except 的最小形状
# ============================================================
print("\n" + "=" * 55)
print("  二、最小形状")
print("=" * 55)

#     try:
#         # 正常流程：你【希望】它成功做的事
#         ...
#     except 某种错误:
#         # 出事了怎么办
#         ...
#
# 执行顺序：
#   try 里的代码一路顺利   → except 整块跳过
#   try 里某一行爆了       → 立刻跳到 except，try 剩下的行不执行
#
# 【关键】except 只处理"这一种错误"，处理完，程序从 try/except 后面继续。

try:
    number = int("abc")          # 这行会抛 ValueError
    print("这一行不会执行")       # ← try 里出错后，后面直接跳过
except ValueError:
    print("  捕获住了：'abc' 不是数字")

print("  程序继续往下走 —— 没有崩")


# ============================================================
# 三、捕获的到底是什么？异常类型表
# ============================================================
print("\n" + "=" * 55)
print("  三、常见异常类型")
print("=" * 55)

# 每个异常都是"一种特定的失败原因"。捕获哪个，取决于你【预料到】哪种错。

cases = [
    ("int('abc')",       lambda: int("abc")),
    ("int('80')/0",      lambda: 1 / 0),
    ("[1,2][5]",         lambda: [1, 2][5]),
    ("{}['missing']",    lambda: {}["missing"]),
    ("open('没有这个')",  lambda: open("没有这个文件.txt")),
    ("'a' + 1",          lambda: "a" + 1),
]

for desc, fn in cases:
    try:
        fn()
        print(f"  {desc:<18} → 没出错")
    except Exception as e:
        # type(e).__name__ 打出异常的类型名
        print(f"  {desc:<18} → {type(e).__name__}: {e}")

# 记不住全部没关系，记住最常撞的这 5 个：
#
#   ValueError          int("abc")   类型对，但值不对
#   ZeroDivisionError   1 / 0        除以零
#   IndexError          lst[99]      下标越界（你的 parts[6] 就是这个）
#   KeyError            d["不存在"]  字典里没这个 key
#   FileNotFoundError   open("x")    文件不存在
#   TypeError           "a" + 1      类型对不上
#
# 【怎么知道该捕获哪个？】
#   报错的最后一行会直接告诉你。照着抄就行：
#       IndexError: list index out of range
#       ^^^^^^^^^^ 抄这个


# ============================================================
# 四、多个 except —— 不同的错，不同的处理
# ============================================================
print("\n" + "=" * 55)
print("  四、多个 except")
print("=" * 55)

def read_port(text):
    """把用户输入转成端口号，并做合法性检查。"""
    try:
        port = int(text)
    except ValueError:
        # 用户输入的根本不是数字
        print(f"    [!] '{text}' 不是数字")
        return None
    except TypeError:
        # 传进来的根本不是字符串（比如 None）
        print(f"    [!] 输入类型不对: {type(text).__name__}")
        return None

    # 注意：合法性检查【不在】 try 里 —— 它不是"异常"，是"业务规则"
    if not 1 <= port <= 65535:
        print(f"    [!] {port} 不在 1-65535 范围内")
        return None

    return port

print("  read_port('8000')  →", read_port("8000"))
print("  read_port('abc')   →", read_port("abc"))
print("  read_port('99999') →", read_port("99999"))
print("  read_port(None)    →", read_port(None))

# 【重点】为什么范围检查没放进 try？
#   异常处理是给【意料之外的失败】用的。
#   端口超出范围是【意料之中的业务规则】，用普通的 if 判断就够了。
#   把业务规则塞进 try/except，会让代码难读，也会掩盖真正的 bug。


# ============================================================
# 五、else 和 finally
# ============================================================
print("\n" + "=" * 55)
print("  五、else 和 finally")
print("=" * 55)

def parse_port(text):
    try:
        port = int(text)
    except ValueError:
        print(f"    [x] '{text}' 解析失败")
    else:
        # try 里【没有出错】才会执行 else
        # 用途：把"只有在成功时才该做的事"跟 try 分开，try 里只放"可能失败的语句"
        print(f"    [+] 解析成功: {port}")
    finally:
        # 【不管成不成功】都会执行。常用于收尾：关文件、释放锁、记日志
        print("    [·] 收尾动作（finally 一定会执行）")

print("  parse_port('443'):")
parse_port("443")
print("  parse_port('abc'):")
parse_port("abc")

# 那 with open 不是已经能自动关文件了吗？
# 是的。finally 真正的用武之地是 with 管不到的东西：
#   释放锁、关闭数据库游标、删除临时文件、写一条"本次运行已结束"的日志。


# ============================================================
# 六、裸 except —— 不要写
# ============================================================
print("\n" + "=" * 55)
print("  六、为什么不要写裸 except")
print("=" * 55)

# ❌ 恶习：
#     try:
#         do_something()
#     except:
#         pass
#
# 问题 1：except: 捕获【所有】异常，包括你压死都想不到的
#         —— 连 KeyboardInterrupt（你按 Ctrl+C）和 SystemExit 都会被吞掉
# 问题 2：pass 什么都不做 —— 出错了你【永远不知道】出过错
# 问题 3：真正的 bug 被藏起来，程序带着错误状态继续跑，结果是错的
#
# 【真实事故的经典形态】
#     上线后数据少了 30%，查了三天，
#     最后发现某处有个 except: pass，把一条插入失败悄悄吞了。
#
# 正确做法：捕获你【明确知道怎么处理】的那几种，其余让它照常报出来。

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("    [!] 除数为 0，返回 None")
        return None
    # 其他异常（比如传了字符串）就让它自然抛出 ——
    # 那不是"已预料的情况"，而是我的代码写错了，应该立刻暴露。

print("  safe_divide(10, 2) →", safe_divide(10, 2))
print("  safe_divide(10, 0) →", safe_divide(10, 0))


# ============================================================
# 七、raise —— 主动报错
# ============================================================
print("\n" + "=" * 55)
print("  七、raise")
print("=" * 55)

def load_targets(filepath):
    """
    读取目标列表。
    文件不存在时，抛一个【说得清楚】的错误，而不是返回空列表。
    """
    p = Path(filepath)
    if not p.exists():
        # 为什么要 raise？
        # 如果这里 return []，调用者会以为"目标列表是空的"，程序照常跑，
        # 结果是"扫描了 0 个目标"，看起来一切正常 —— 这是最危险的情况。
        # 抛错 = 立刻让问题暴露出来，而不是让它悄悄变成错误的结果。
        raise FileNotFoundError(f"目标文件不存在: {filepath}")

    targets = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                targets.append(line)
    return targets

try:
    load_targets("这个文件不存在.txt")
except FileNotFoundError as e:
    print(f"  捕获: {e}")

# 【原则】
#   能处理的错 → 捕获，给出替代方案（跳过、重试、默认值）
#   不能处理的错 → 让它抛出去，越早暴露越好
#   悄悄吞掉的错 → 永远不要这么做


# ============================================================
# 八、pathlib —— 路径不该用字符串拼
# ============================================================
print("\n" + "=" * 55)
print("  八、pathlib")
print("=" * 55)

# 以前你可能这样写：
#     "reports/" + name + ".json"
#
# 问题：Windows 用 \ ，Linux 用 / ；少写一个斜杠就出错；
#       想取"文件名不带扩展名"得自己写字符串处理。
#
# pathlib.Path 把路径当成【对象】而不是字符串，这些问题一次解决。

p = Path(__file__)          # 当前这个 .py 文件自己的路径
print(f"  完整路径 : {p}")
print(f"  所在目录 : {p.parent}")
print(f"  文件名   : {p.name}")
print(f"  不带后缀 : {p.stem}")
print(f"  后缀     : {p.suffix}")

target = Path("data") / "report.json"     # 用 / 拼路径，自动处理分隔符
print(f"  拼出来的路径: {target}")

# 常用方法：
#   p.exists()        存在吗
#   p.is_file()       是文件吗
#   p.mkdir()         建目录
#   p.open(...)       打开（和内置 open 一样，配合 with 用）
#
# 【关键】Path 对象可以直接传给 open()，也能直接传给 with。
# 所以你项目里的 open(filepath) 完全不用改 —— filepath 传 Path 也行。


# ============================================================
# 九、练习
# ============================================================
print("\n" + "=" * 55)
print("  九、练习")
print("=" * 55)

# ------------------------------------------------------------
# 练习 A：给崩溃代码加保护
# ------------------------------------------------------------
# 【背景】
# 日志分析器要把每一行切成若干段，第 7 段（parts[6]）是访问路径。
# 下面这 4 行里，混进了 2 行坏数据。

messy_lines = [
    'a b c d e f /ok',
    '',
    'a b',
    'a b c d e f /also-ok',
]

# 【第一步：先看它怎么崩】
# 把下面三行取消注释，运行一次。记住两件事：
#   - 它崩在第几行数据上
#   - 报的是什么异常
#
#     for line in messy_lines:
#         parts = line.split()
#         print(f"  ok: {parts[6]}")
#
# 【第二步：改写它，满足这 4 条】
#   1. 遇到坏行【跳过】，继续处理下一行，程序不能崩
#   2. 正常行打印：  ok: <parts[6] 的值>
#   3. 坏行不打印，但要计数
#   4. 循环结束后输出一行汇总：  正常 N 行，坏行 M 行
#
# 【预期输出】（必须完全一致）
#   ok: /ok
#   ok: /also-ok
#   正常 2 行，坏行 2 行
#
# 【验收标准】
#   □ 程序跑完，不抛异常
#   □ 恰好输出两行 ok，内容和顺序都对
#   □ 汇总数字是 2 和 2
#   □ 用了 try + except IndexError

# === 你的代码写在这里 ===
bad_line = 0
good_line = 0
for line in messy_lines:
    try:
        parts = line.split()
        print(f"  ok: {parts[6]}")
        good_line += 1
    except IndexError:
        bad_line += 1
print(f"正常 {good_line} 行, 坏行 {bad_line} 行")


# ------------------------------------------------------------
# 练习 B：友好的文件读取
# ------------------------------------------------------------
# 【任务】写一个函数 read_targets(filepath)，返回目标列表。
#
# 【行为要求】
#   1. 文件存在：
#        - 逐行读取，去掉首尾空白（strip）
#        - 跳过空行
#        - 跳过以 # 开头的行
#        - 其余行装进列表，返回
#
#   2. 文件不存在：
#        - 打印一行提示：  [!] 文件不存在: <filepath>
#        - 返回空列表 []          ← 注意：这里【不抛异常】，而是吞掉
#
# 【为什么这次不 raise？】
#   上一节 load_targets 要求"文件不在就大喊"，因为扫描任务是
#   客户明确指派的，没目标 = 出了大事，必须让人知道。
#   这一次客户的要求是"没有这个文件就当没有目标，继续跑"。
#
#   同一件事，两种处理方式都对 —— 取决于调用者想要什么。
#   这是设计函数时的关键判断，不是语法问题。
#
# 【自测】
#   read_targets("targets.txt")     → 应该返回 5 个 IP 的列表
#   read_targets("不存在.txt")       → 打印提示，返回 []
#
#   targets.txt 的内容（第一行是注释，应被跳过）：
#       # 目标列表
#       192.168.1.1
#       192.168.1.2
#       192.168.1.3
#       10.0.0.1
#       172.16.0.1
#
# 【验收标准】
#   □ 文件存在时，返回长度正好为 5 的列表，不含注释行
#   □ 文件不存在时，程序不崩溃，打印提示，返回 []
#   □ 实现里用到了 try/except FileNotFoundError，或 Path.exists()

# === 你的代码写在这里 ===
def read_target(filepath):
    report = []

    try: 
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    report.append(line)
    except FileNotFoundError:
        print(f"   [!] 文件不存在: {filepath}")
        return []
    
    return report

report = read_target("targets.txt")
print(report)
read_target("不存在.txt")


# ------------------------------------------------------------
# 练习 C：批量解析 + 容错
# ------------------------------------------------------------
# 【背景】
# 端口配置从网页表单/配置文件里来的，用户什么都可能输。
# 你要批量转成 int，转不动的不能拖垮整批。

raw_ports = ["22", "80", "abc", "443", "", "8080", " 3306 ", "99999999999999"]

# 【任务】
# 遍历 raw_ports，把每一项转成 int：
#   - 成功 → 追加到 good 列表（保持原顺序）
#   - 失败 → 追加到 failed 列表
#         并且【当场】打印一行：  [!] 无法转换: <原值，用 repr 显示>
#
# 最后打印三行：
#   成功: [ ... ]
#   失败: [ ... ]
#   成功率: NN.NN%
#
# 【预期输出】（顺序和空格必须一致）
#   [!] 无法转换: 'abc'
#   [!] 无法转换: ''
#   成功: [22, 80, 443, 8080, 3306, 99999999999999]
#   失败: ['abc', '']
#   成功率: 75.00%
#
# 【两个容易错的地方】
#   1. int(" 3306 ") 是【能成功】的 —— int 会自动去掉首尾空白
#   2. int("99999999999999") 也是【能成功】的 —— Python 整数没有上限
#      ⚠️ 但它不是合法端口（> 65535）。这说明：
#         "转换成功" ≠ "值合法"。两件事，不要混。
#
# 【验收标准】
#   □ 两个无法转换的值被打印出来，用 repr 显示（带引号）
#   □ good 的长度是 6，failed 的长度是 2
#   □ 成功率打印成 75.00%
#   □ 用了 try / except ValueError

# === 你的代码写在这里 ===
print("\n")

def read_ports(ports):
    good = []
    failed = []
    for port in ports:
        try:
            good.append(int(port))
        except ValueError:
            failed.append(port)
            print(f"   [!] 无法转换: {port!r}")

    print(f"   成功: {good}")
    print(f"   失败: {failed}")
    print(f"   成功率: {len(good) / len(ports) * 100 :.2f}%")

read_ports(raw_ports)

# ------------------------------------------------------------
# 练习 D：升级你的项目（重点，做在 project_01_log_analyzer.py 里）
# ------------------------------------------------------------
# 任务：回到 project_01_log_analyzer.py，让它在遇到坏行时不崩溃。
#
#   1. count_by_ip 和 find_suspect_ips 里，把可能出错的部分包进 try
#   2. 坏行要【计数】，最后打印 "跳过 N 行坏数据"
#   3. 生成一个 bad_access.log（含几条坏行），验证程序不会崩
#
#   自测标准：往 access.log 里插一行 "坏数据"，程序必须正常跑完，
#            并且在输出里告诉你跳过了几行。
#
# 【为什么这一步最重要】
#   这样改完，你的项目才第一次具备"能接触真实数据"的资格。
#   在此之前，它只在你自己的干净文件上跑得动 —— 那叫 demo，不叫工具。


# ============================================================
# 参考答案（先自己做，卡住了再看）
# ============================================================

# ---- 练习 A ----
# good = 0
# bad = 0
# for line in messy_lines:
#     try:
#         parts = line.split()
#         print(f"  ok: {parts[6]}")
#         good += 1
#     except IndexError:
#         bad += 1
# print(f"正常 {good} 行，坏行 {bad} 行")

# ---- 练习 B ----
# def read_targets(filepath):
#     p = Path(filepath)
#     if not p.exists():
#         print(f"  [!] 文件不存在: {filepath}")
#         return []
#     targets = []
#     with p.open("r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if line and not line.startswith("#"):
#                 targets.append(line)
#     return targets

# ---- 练习 C ----
# good = []
# failed = []
# for raw in raw_ports:
#     try:
#         good.append(int(raw))
#     except ValueError:
#         failed.append(raw)
#         print(f"  [!] 无法转换: {raw!r}")
# print(f"成功 {good}")
# print(f"失败 {failed}")
# rate = len(good) / len(raw_ports) * 100
# print(f"成功率: {rate:.2f}%")

# ---- 练习 D ----
# 在 count_by_ip 里：
#     bad_lines = 0
#     for line in f:
#         try:
#             parts = line.split()
#             ip = parts[0]
#         except IndexError:
#             bad_lines += 1
#             continue
#         if ip in count:
#             count[ip] += 1
#         else:
#             count[ip] = 1
#
# 更简单的判断（不靠异常）：
#     parts = line.split()
#     if len(parts) < 7:      # 字段不够，直接当坏行
#         bad_lines += 1
#         continue
#
# 【两种写法怎么选？】
#   len(parts) < 7  → 更直白，能明确表达"我要至少 7 个字段"
#   try/except      → 更通用，不关心"为什么坏"
#   实际工程里两个都用，甚至一起用：先判断长度，再用 try 兜底。
