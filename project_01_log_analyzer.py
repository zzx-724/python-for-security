"""
项目 01：访问日志分析器  —— 你的第一个完整工程
客户需求（原文）：

    "服务器日志在这儿（access.log），帮我看看哪些 IP 访问太频繁了，
     可疑的挑出来，存个报告给我。"

就这一句。没有提示，没有步骤，没有答案。

────────────────────────────────────────────────────────────
工作约定（这次不许违反）
────────────────────────────────────────────────────────────

1. 【我只反问，不给代码】
   你卡住了，我会先问你"你觉得这一步要做什么"，不会直接甩代码给你。

2. 【你要这样问】
   别只说"不会"。用这个格式说清楚：
       - 我在做第几步
       - 我想让它干什么
       - 我试了什么，现在是什么现象（贴报错）
   把问题说清楚，本身就是工程能力的一部分。

3. 【真卡死了怎么办】
   直接说"我完全没思路"。我会给你一个【方向】或【去查什么关键词】，
   但仍然不给代码。

────────────────────────────────────────────────────────────
开工前的三个动作（这是方法，不是答案）
────────────────────────────────────────────────────────────

动作 1：先别写代码。用中文把这件事分成几步，写在纸/便签上。
        比如"第一步干什么，第二步干什么"。

动作 2：先写一个【能跑通的最小版本】。
        不要想着一口气写完。第一版只需要做到"能打开文件、打印第一行"。
        能跑 → 再往下加。不能跑 → 先弄到能跑。

动作 3：一步一运行。
        每加一小块就运行一次。一运行就报错 → 错就在你刚加的那块。
        攒了 50 行才运行 → 错在哪儿你根本不知道。

────────────────────────────────────────────────────────────
你手里已经有的工具（Day 1-6 全都能用）
────────────────────────────────────────────────────────────
    读文件 / 写文件        Day 6
    字符串拆分、清理        Day 2   (split / strip / startswith)
    列表、字典、集合        Day 3
    循环、推导式、enumerate Day 4
    def / return            Day 5

够了。真的够了。刚才演示过。

────────────────────────────────────────────────────────────
交付标准（客户验收时会看这几条）
────────────────────────────────────────────────────────────
    □ 能从 access.log 读出所有记录
    □ 能统计出【每个 IP 各访问了多少次】
    □ 能按访问次数从多到少打印出来
    □ 能看出哪个/哪几个 IP 明显异常
    □ 结果存成一个 JSON 文件

注意：需求里【没有】说"按次数排序"、"找出可疑的"具体怎么做。
   那是你作为工程师要自己决定的 —— 这就是"拆解"。

开始吧。
"""

# ============================================================
# 你的代码写在这里。从"打印第一行"开始。
# ============================================================

import json

#----------配置----------
LOG_FILE = "access.log"
SENSITIVE_PATH = ["/.git/config", "/.env", "/backup.zip", "/phpmyadmin", "/wp-admin", "/admin"]
THRESHOLD = 15
REPORT_FILE = "final_report.json"

#----------工具----------
def load_records(filepath):
   bad_lines = 0
   records = []
   with open(filepath, "r", encoding="utf-8") as f:
      for line in f:
         parts = line.split()
         if len(parts) < 7:
            bad_lines += 1
            continue

         records.append({
            "ip": parts[0],
            "path": parts[6]
         })

   return records, bad_lines

def count_by_ip(records):
   count = {}
   for rec in records:
      ip = rec["ip"]
      if ip in count:
         count[ip] += 1
      else:
         count[ip] = 1

   return count

def find_suspect_ips(records, paths):
   suspects = set()
   for rec in records:
      ip = rec["ip"]
      path = rec["path"]
      if path in paths:
         suspects.add(ip)
   return suspects

def sort_counts(counts):
   ranked = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
   return ranked

def print_table(ranked, suspects, threshold):
   for ip,count_1 in ranked:
      if count_1>=threshold or ip in suspects:
         print(f"ip:{ip:>15}     访问次数:{count_1:>5} <----------可疑!")
      else:
         print(f"ip:{ip:>15}     访问次数:{count_1:>5}")
   print(f"访问敏感路径的ip: {suspects}")

def build_report(ranked, suspects, threshold):
   report = []
   for ip,n in ranked:
      if n >= threshold:
         reason = "访问次数超过阈值"
      elif ip in suspects:
         reason = "访问了敏感路径"
      else:
         continue

      report.append({
         "ip": ip,
         "count": n,
         "reason": reason
      })
   return report

def save_report(report, save_path):
   with open(save_path, "w", encoding="utf-8") as f:
      json.dump(report, f, ensure_ascii=False, indent=2)

#----------主函数----------
def main():
   try:
      records, bad_lines = load_records(LOG_FILE)
   except FileNotFoundError as e:
      print(f"   [!] 拿不到日志文件, 任务无法继续")
      print(f"   原因: {e}")
      return
   count = count_by_ip(records)
   suspects = find_suspect_ips(records, SENSITIVE_PATH)
   ranked = sort_counts(count)
   print_table(ranked, suspects, THRESHOLD)
   print(f"跳过 {bad_lines} 行坏数据")
   report = build_report(ranked, suspects, THRESHOLD)
   save_report(report, REPORT_FILE)

main()