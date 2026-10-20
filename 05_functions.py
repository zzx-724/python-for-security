"""
Day 5: 函数 — 从"写脚本"到"造工具"

为什么函数是分水岭？
  Day 1-4 你写的是"一次性脚本"：从头到尾一条道跑到底，跑完就完了。
  Day 5 开始你能"造工具"：把一段逻辑打包、起个名字，想用就调用。

先看看你的痛点（Day 4 专项练习 3、5、6）：

    练习 3:  for i, port in enumerate(ports_3, 1):
                 print(f"{i}. {port:<6} {mark}")
    练习 5:  for ip, port, status in zip(ips_5, ports_5, status_5):
                 print(f"{ip:<15} {port:<6} {status}")
    练习 6:  for port, service in zip(ports_6, services_6):
                 print(f"{port:>4}      {service}")

  三段代码几乎一样，都在"打印一张对齐的表格"，你抄了三遍。
  抄写的三个代价：
    1. 想改格式（比如空格改成制表符），要改三处，漏一处就乱
    2. 变量名越用越紧（ports_2 就被你用了两次，撞车了）
    3. 代码越写越长，找 bug 越来越难

  函数就是解决这三件事的：写一次，起个名字，到处调用。

C 语言对比：
  C:      int add(int a, int b) { return a + b; }
  Python: def add(a, b):
              return a + b

  Python 不写返回类型、不写参数类型、不写大括号 —— 靠缩进划分代码块。
"""


# ============================================================
# 一、定义和调用 — 给一段逻辑起个名字
# ============================================================
print("=" * 50)
print("  一、定义和调用")
print("=" * 50)

# 结构：
#   def  函数名 (参数列表):
#       函数体（缩进 4 格）
#       return 返回值

def greet(target):
    """给一个目标打个招呼 —— 这是最简单的函数"""
    print(f"  [*] 准备扫描目标: {target}")


# ⚠️ 最关键的一句话：定义 ≠ 执行
# 上面那段 def 只是"告诉 Python 有这么个函数"，它一行都不会跑。
# 必须【调用】才会执行：

print("调用 1 次:")
greet("192.168.1.1")

print("调用 3 次:")
greet("192.168.1.1")
greet("192.168.1.2")
greet("192.168.1.3")

# 看明白了吗？【写一次，用三次】。
# 这就是函数最朴素的价值 —— 但远远不止于此。

# C 对比：
#   C 里函数要"先声明后使用"（或者在头文件里声明）。
#   Python 里 def 本身就是定义，不用单独声明，但顺序仍然不能反：
#   必须【先 def，后调用】，写在定义前面会报 NameError。


# ============================================================
# 二、return vs print — 最容易搞混的一对（重点！）
# ============================================================
print("\n" + "=" * 50)
print("  二、return vs print")
print("=" * 50)

# 这两个看着都在"输出"，其实是完全不同的两件事：
#
#   print  = 【给人看】把东西显示在屏幕上，然后……就没有然后了
#   return = 【给程序用】把结果交还给调用者，可以接着拿它做运算

def add_print(a, b):
    print(f"  print 版: {a + b}")     # 只打印，没交回任何东西

def add_return(a, b):
    return a + b                      # 把结果交回去

# --- 实验 1：print 版的结果能存下来吗？---
add_print(2, 3)                       # 屏幕显示 5
x = add_print(2, 3)                   # 屏幕还是显示 5
print(f"  把 print 版的结果存进 x，x = {x}")     # x = None ！

# 为什么是 None？因为 add_print 没有 return，
# 【没有 return 的函数，一律返回 None】

# --- 实验 2：return 版的结果能存下来 ---
y = add_return(2, 3)
print(f"  把 return 版的结果存进 y，y = {y}")    # y = 5 ✅

# --- 实验 3：真正的区别在这里 —— 能不能"接着用"---
print(f"  return 版能继续运算: {add_return(2, 3) * 10}")     # 50 ✅

# print 版不行，取消下面这行的注释试试：
# print(f"  print 版能继续运算: {add_print(2, 3) * 10}")
# 报错：TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
# 翻译过来：None 和数字不能相乘。因为 add_print 交回来的是 None，不是 5。

# 【判断该用哪个】问自己一句话：
#   "算出来的这个东西，后面还要用吗？"
#     要用  → return
#     只是显示给人看 → print
#
# 在安全脚本里的体现：
#   写报告给用户看  → print
#   算出开放的端口列表交给下一步处理 → return
#   真正专业的函数，通常是 return 出去，由调用方决定 print 什么

# C 对比：
#   C 的 void 函数 = Python 里没有 return 的函数（都返回"空"）
#   区别：C 的 void 是真的不能赋值，Python 的 None 是个真实的值，可以存、可以判断


# ============================================================
# 三、参数 — 默认值让调用更省事
# ============================================================
print("\n" + "=" * 50)
print("  三、参数")
print("=" * 50)

# --- 3.1 默认参数 ---
# 场景：扫描超时通常用 3 秒，但偶尔某个慢目标要调成 10 秒。
# 不可能每次都写超时参数 —— 给个默认值。

def scan_port(ip, port, timeout=3):
    """
    模拟端口扫描
    timeout 有默认值 3，调用方【可以不传】
    """
    print(f"    扫描 {ip}:{port} (超时={timeout}秒)")

print("不传 timeout（用默认值 3）:")
scan_port("10.0.0.1", 80)

print("传 timeout（覆盖默认值）:")
scan_port("10.0.0.1", 80, 10)

# ⚠️ 规则：有默认值的参数必须放在【后面】
#      def f(a, b=1)      ✅
#      def f(a=1, b)      ❌ SyntaxError: non-default argument follows default argument

# --- 3.2 关键字参数：按名字传，顺序随便 ---
print("\n关键字参数（顺序可以打乱）:")
scan_port(port=80, ip="10.0.0.1")                  # 顺序反了也照样对
scan_port("10.0.0.1", timeout=5, port=443)         # 混着用也行

# 为什么要这个？—— 参数一多，位置就容易记混。
# 看看这行调用，如果不写参数名，你知道哪个是哪个吗？
#      scan_host("10.0.0.1", [22, 80], 3, True)
# 写成关键字就很清楚：
#      scan_host(ip="10.0.0.1", ports=[22, 80], timeout=3, verbose=True)
#
# 【建议】参数超过 3 个时，调用时就写参数名 —— 三个月后你自己都记不住顺序。


# ============================================================
# 四、作用域 — 函数里的变量，外面看不见
# ============================================================
print("\n" + "=" * 50)
print("  四、作用域")
print("=" * 50)

# 这是新手最容易懵的地方，用实验看清楚。

counter = 0          # 这个变量定义在【函数外面】= 全局变量


def try_increase():
    counter = 100    # ⚠️ 这不是"修改外面的 counter"，而是【新建了一个同名变量】
    print(f"  函数内看到的 counter: {counter}")

try_increase()
print(f"  函数外看到的 counter: {counter}")     # 还是 0 ！

# 发生了什么？两个 counter 是【两个不同的变量】：
#   函数外的 counter  = 0（一直没变）
#   函数内的 counter  = 100（函数跑完就销毁了，外面根本看不到）
#
# C 对比：和 C 的局部变量规则一样 —— 函数里定义的变量，出了函数就没了。

# --- 那函数怎么把结果传出来？---
# 答案就是 return，这是唯一（也是最好的）通道：
count = 0

def increase(n):
    """接收 n，返回 n+1 —— 通过 return 把结果送出来"""
    return n + 1

count = increase(count)      # 用返回值覆盖原变量
count = increase(count)
print(f"  通过 return 累加: {count}")      # 2

# 【核心结论】函数和外界交换数据的通道只有两个：
#   入口：参数   →  外面把数据【送进去】
#   出口：return →  函数把结果【送出来】
# 中间的局部变量，外界完全看不到。这叫【封装】—— 以后你会知道这是好事：
# 别人用你的函数，只需要关心"传什么进去、拿什么出来"，不用管里面怎么实现的。


# ============================================================
# 五、函数调用函数 + 文档字符串
# ============================================================
print("\n" + "=" * 50)
print("  五、函数调用函数")
print("=" * 50)

# 复杂的工具都是"小函数拼起来"的。
# 规则：一个函数只干一件事，然后用别的函数把它们串起来。

def get_service(port):
    """端口 → 服务名（查不到就返回 unknown）"""
    services = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
    return services.get(port, "unknown")     # Day 3 学的 .get()，防崩溃


def is_web_port(port):
    """判断是不是 Web 端口，返回 True / False"""
    return port in (80, 443, 8080, 8443)      # 直接返回比较结果


def describe_port(port):
    """给一个端口，返回一句描述 —— 这个函数【调用了上面两个函数】"""
    service = get_service(port)               # 调用函数 1
    if is_web_port(port):                     # 调用函数 2
        return f"{port} → {service}（Web 服务，重点关注）"
    return f"{port} → {service}"


for p in [22, 80, 3306, 9999]:
    print(f"  {describe_port(p)}")

# 为什么这样写比"一个大函数塞到底"好？
#   1. get_service 单独拿出来，别的地方也能用
#   2. is_web_port 逻辑变了只改一处
#   3. 每个函数都短，一眼看懂

# --- 文档字符串 docstring ---
# 你注意到每个函数下面的 """...""" 了吗？那不是注释，是【文档字符串】。
# 它会被 Python 记住，别人（和 IDE）能查到：
print(f"\n  describe_port 的说明: {describe_port.__doc__}")

# 在 VS Code 里，调用函数时把鼠标悬停在名字上，就会显示这段说明。
# 【习惯】每个函数都写一句"这个函数干什么、返回什么"，一行就够。


# ============================================================
# 六、练习（你来写）
# ============================================================
print("\n" + "=" * 50)
print("  六、练习")
print("=" * 50)

# ------------------------------------------------------------
# 练习 A：return 基础
# ------------------------------------------------------------
# 任务：写一个函数 is_high_risk(port)，判断端口是不是高危
#       高危端口：21, 22, 23, 445, 1433, 3306, 3389
#       返回 True 或 False（注意：是 return，不是 print！）
#
# 写完后用这两行测试：
#     print(is_high_risk(22))     # 应该输出 True
#     print(is_high_risk(80))     # 应该输出 False

# === 你的代码写在这里 ===
def is_high_risk(port):
    if port in (21,22,23,445,1433,3306,3389):
        return True
    else:
        return False

print(f"22端口是否高危: {is_high_risk(22)}")
print(f"80端口是否高危: {is_high_risk(80)}")


# ------------------------------------------------------------
# 练习 B：把"抄了三遍的表格"封成函数
# ------------------------------------------------------------
# 这就是开头说的那个痛点。现在把它彻底解决。

# 任务 1：写一个函数 format_row(ip, port, status)
#         返回一行对齐的字符串，格式：IP 占 15 格左对齐，端口占 6 格，状态跟在后面
#         （提示：f"{ip:<15} {port:<6} {status}"，注意是 return 不是 print）
#
# 任务 2：写完之后，用下面三个列表调用它，打印出对齐的表格
#         并在最后打印一行统计：开放了几个

ips_b = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
ports_b = [22, 80, 443]
status_b = ["open", "closed", "open"]

# === 你的代码写在这里 ===
def format_row(ip, port, status):
    return f"{ip:<15} {port:<6} {status}"
print(format_row("192.168.1.1",22,"open"))

print("\n")
count_1 = 0
for ip,port,status in zip(ips_b,ports_b,status_b):
    if status == "open":
        count_1+=1
    print(format_row(ip,port,status))
print(f"开放了 {count_1} 个端口")

# ------------------------------------------------------------
# 练习 C：函数调用函数
# ------------------------------------------------------------
# 任务 1：写一个函数 classify(port)，返回端口类别：
#           Web 端口（80/443/8080/8443）  → 返回 "web"
#           数据库端口（3306/1433/5432）  → 返回 "db"
#           其他                          → 返回 "other"
#
# 任务 2：写一个函数 build_report(ports)，接收端口列表
#           遍历它，对每个端口调用 classify()
#           返回一个列表，里面是 (端口, 类别) 这样的元组
#
#         预期：build_report([80, 3306, 9999])
#               返回 [(80, 'web'), (3306, 'db'), (9999, 'other')]
#
# 提示：怎么造出 (端口, 类别) 元组？直接写 (port, classify(port))
#       收集到列表里用 Day 3 学的 append()

# === 你的代码写在这里 ===
def classify(port):
    web_port = (80,443,8080,8443)
    database_port = (3306,1433,5432)
    if port in web_port:
        return "web"
    elif port in database_port:
        return "db"
    else:
        return "other"


def build_report(ports):
    report = []
    for port in ports:
        report.append((port,classify(port)))
    return report

print(f"{build_report([80, 3306, 9999])}")

# ------------------------------------------------------------
# 练习 D：找 bug（判断 return 用错的地方）
# ------------------------------------------------------------
# 下面这个函数是别人写的，意图是"算出端口数量的两倍"。
# 但它有个 bug，你来找出问题在哪，并改对。

def double_count_wrong(ports):
    """返回端口数量的两倍"""
    print(len(ports) * 2)

# 测试代码（先跑一下看看会怎样）：
#     result = double_count_wrong([22, 80, 443])
#     print(f"结果是: {result}")
#     print(f"再加 1 是: {result + 1}")

# 问题 1：屏幕上会打印出什么数字？
# 问题 2：result 的值是什么？
# 问题 3：最后一行会报什么错？为什么？
# 问题 4：怎么改才对？

# === 你的答案写在这里 ===
#1:6
#2:None,因为函数没有 return
#3:TypeError，NoneType 和 int 不能相加
def double_count(ports):
    """返回端口数量的两倍"""
    return len(ports) * 2

# ============================================================
# 参考答案（先自己写！写完再对照）
# ============================================================
# 练习 A
# def is_high_risk(port):
#     """判断端口是否高危"""
#     return port in (21, 22, 23, 445, 1433, 3306, 3389)
#
#
# print(is_high_risk(22))     # True
# print(is_high_risk(80))     # False
#
# 【要点】直接 return 比较结果就行，不用写 if/else：
#     if port in (...):  return True
#     else:              return False
#   这两行等于上面那一行。因为 `port in (...)` 本身就已经是 True/False 了。
#
# 练习 B
# def format_row(ip, port, status):
#     """返回一行对齐的扫描结果"""
#     return f"{ip:<15} {port:<6} {status}"
#
#
# open_count = 0
# for ip, port, status in zip(ips_b, ports_b, status_b):
#     print(format_row(ip, port, status))
#     if status == "open":
#         open_count += 1
# print(f"开放 {open_count} 个端口")
#
# 【要点】format_row 只负责"造字符串"，不负责打印。
#   这就叫【职责单一】—— 打印由调用方决定，这个函数在别处也能用
#   （比如以后要写进文件、要塞进 JSON，都不用改它）。
#
# 练习 C
# def classify(port):
#     """返回端口类别"""
#     if port in (80, 443, 8080, 8443):
#         return "web"
#     elif port in (3306, 1433, 5432):
#         return "db"
#     else:
#         return "other"
#
#
# def build_report(ports):
#     """接收端口列表，返回 (端口, 类别) 的列表"""
#     report = []
#     for port in ports:
#         report.append((port, classify(port)))    # 调用 classify
#     return report
#
#
# print(build_report([80, 3306, 9999]))
# # [(80, 'web'), (3306, 'db'), (9999, 'other')]
#
# 【要点】build_report 里没有重复"判断端口属于哪类"的逻辑，
#   它直接调用 classify。这样以后加新类别（比如 "mail"），只改 classify 一个地方。
#
# 练习 D
# 问题 1：屏幕打印 6（3 个端口 × 2）
# 问题 2：result 是 None（函数没有 return）
# 问题 3：TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
#         因为 None 不能和数字相加
# 问题 4：把 print 改成 return：
#
#     def double_count(ports):
#         """返回端口数量的两倍"""
#         return len(ports) * 2
#
# 【判断口诀】"算出来的东西后面还要用吗？" 要用就必须 return。
