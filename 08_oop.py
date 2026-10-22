"""
Day 8：面向对象 —— 把代码从「一堆函数」改成「一个对象」

今天只做两件事：
  练习 A：写一个小类 IPCounter，搞懂 self 和"每个实例有自己的数据"
  练习 B：把 project_01_log_analyzer.py 重构成 LogAnalyzer 类

规则：卡住了按格式说（我在做哪个方法 / 想让它干什么 / 试了什么、现在什么现象），
     我反问，不给代码。
"""


# ============================================================
# 练习 A：IPCounter（约 20 分钟）
# ============================================================
# 目标：
#   a = IPCounter()
#   a.add("1.1.1.1") 三次，a.add("2.2.2.2") 一次
#   a.top(1)  ->  [("1.1.1.1", 3)]
#   a.top(2)  ->  按次数降序的两个元组
#
# 必须验证：两个实例互不干扰
#   a = IPCounter()
#   b = IPCounter()
#   a.add("1.1.1.1")
#   print(b.top(1))     # 必须是 []，不能是 [("1.1.1.1", 1)]
#
# 提示（不是答案）：
#   - 字典要建在 __init__ 里，不是建在类里
#   - top() 要排序，参考 Day 4 的 sorted(key=...)
#   - self.xxx 是"挂在这个实例身上的数据"；不带 self 的变量函数一结束就没了


class IPCounter:
    def __init__(self):
        # TODO: 建一个空字典，挂到 self 上
        pass

    def add(self, ip):
        # TODO: ip 已经在字典里就 +1，不在就设成 1
        pass

    def top(self, n):
        # TODO: 按次数从多到少排序，返回前 n 个 (ip, 次数) 元组
        pass


# ---- 练习 A 的验证：写完后取消注释，一行一行跑 ----
# a = IPCounter()
# b = IPCounter()
# a.add("1.1.1.1")
# a.add("1.1.1.1")
# a.add("1.1.1.1")
# a.add("2.2.2.2")
# print(a.top(1))      # 期望 [('1.1.1.1', 3)]
# print(a.top(2))      # 期望 [('1.1.1.1', 3), ('2.2.2.2', 1)]
# print(b.top(1))      # 期望 []


# ============================================================
# 练习 B：把项目 01 重构成 LogAnalyzer（约 40 分钟）
# ============================================================
# 打开 project_01_log_analyzer.py 对照着改。
# 验收：python 08_oop.py 的输出，必须和 python project_01_log_analyzer.py 完全一致。
#
# 三个设计问题，自己回答（写在注释里也行）：
#   1. count 每次都 return 出去，还是存成 self.count？
#      提示：build_report 要用它吗？要用的话，每次派人送过去方便，还是挂在对象身上方便？
#   2. __init__ 里除了存参数，要不要顺手把 self.count = {} 也初始化？
#      提示：想想练习 A 里 b.top(1) 为什么必须是 []。
#   3. run() 里的 try/except FileNotFoundError 包住哪几行？
#      提示：MISTAKES.md 第 16 条 —— try 要包住真正抛错的那一行。


class LogAnalyzer:
    def __init__(self, filepath, sensitive_paths, threshold):
        # TODO: 三个参数存成 self.xxx
        # TODO: 想一想 —— 这里要不要把 self.count / self.bad_lines 先初始化？
        pass

    def count_by_ip(self):
        """统计每个 IP 的访问次数，同时数坏行"""
        pass

    def find_suspects(self):
        """返回访问过敏感路径的 IP 集合"""
        pass

    def build_report(self):
        """返回要写进 JSON 的那个列表"""
        pass

    def save_report(self, path):
        """把报告写成 JSON 文件"""
        pass

    def run(self):
        """串起来：try/except 放哪？打印和保存的先后顺序是什么？"""
        pass


# ---- 练习 B 的入口：run() 写好后取消注释 ----
# if __name__ == "__main__":
#     LOG_FILE = "access.log"
#     SENSITIVE_PATH = ["/.git/config", "/.env", "/backup.zip",
#                       "/phpmyadmin", "/wp-admin", "/admin"]
#     THRESHOLD = 15
#
#     analyzer = LogAnalyzer(LOG_FILE, SENSITIVE_PATH, THRESHOLD)
#     analyzer.run()
