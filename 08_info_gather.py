"""
Day 7-8: 阶段一综合项目 — 信息收集工具
把前面 6 天学的全部组合成一个完整的工具

功能：
1. 从文件读取目标列表
2. 模拟 HTTP 请求（检查 URL 是否可访问）
3. 提取页面标题
4. 支持命令行参数
5. 输出 JSON 报告

命令行用法：
  python 07_info_gather.py targets.txt
  python 07_info_gather.py targets.txt -o report.json --timeout 5
"""

import json
import sys
import re
import time
import random
from pathlib import Path

# ============================================================
# 1. 参数解析（简易版，不用 argparse 库也能跑）
# ============================================================


def parse_args():
    """
    解析命令行参数
    例如：python 07_info_gather.py urls.txt -o output.json --timeout 5
    """
    args = {
        "target_file": None,
        "output": "report.json",
        "timeout": 3,
    }

    argv = sys.argv[1:]  # 跳过脚本名
    i = 0
    while i < len(argv):
        if argv[i] in ("-o", "--output"):
            args["output"] = argv[i + 1]
            i += 2
        elif argv[i] in ("-t", "--timeout"):
            args["timeout"] = int(argv[i + 1])
            i += 2
        elif not argv[i].startswith("-"):
            args["target_file"] = argv[i]
            i += 1
        else:
            print(f"[!] 未知参数: {argv[i]}")
            i += 1

    return args


# ============================================================
# 2. 目标加载
# ============================================================


def load_urls(filepath):
    """从文件加载 URL 列表"""
    urls = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if line and not line.startswith("#"):
                    # 自动补全 http://
                    if not line.startswith("http"):
                        line = "http://" + line
                    urls.append(line)
        print(f"[+] 加载 {len(urls)} 个目标")
    except FileNotFoundError:
        print(f"[!] 文件不存在: {filepath}")
        sys.exit(1)
    return urls


# ============================================================
# 3. 信息收集核心逻辑
# ============================================================


def probe_url(url, timeout=3):
    """
    探测一个 URL（模拟 HTTP 请求，实际用 requests 库）
    返回: {"url": ..., "status": ..., "title": ..., "server": ..., "response_time": ...}
    """
    result = {
        "url": url,
        "status": None,
        "title": None,
        "server": None,
        "response_time": 0,
        "error": None,
    }

    print(f"  [*] 探测 {url} ... ", end="")

    try:
        # 模拟网络请求时间
        response_time = random.uniform(0.1, timeout)
        time.sleep(min(response_time * 0.1, 0.3))  # 模拟延迟

        # 模拟响应
        status = random.choice(
            [200, 200, 200, 200, 200, 301, 302, 403, 404, 404, 404, 500]
        )

        result["response_time"] = round(response_time, 3)
        result["status"] = status

        # 模拟提取标题
        fake_titles = {
            200: ["Admin Panel", "Welcome to nginx", "Apache2 Default Page", "Dashboard"],
            301: [None],
            302: [None],
            403: [None],
            404: [None],
            500: [None],
        }
        title = random.choice(fake_titles.get(status, [None]))
        result["title"] = title

        # 模拟 Server 头
        fake_servers = ["Apache/2.4.41", "nginx/1.18.0", "IIS/10.0", "Cloudflare"]
        result["server"] = random.choice(fake_servers) if status in (200, 403) else None

        # 输出图标
        icons = {200: "[+]", 301: "[~]", 302: "[~]", 403: "[!]", 404: "[-]", 500: "[!]"}
        status_text = f"{status}" + (f" ({title})" if title else "")
        print(f"{icons.get(status, '[?]')} {status_text}")

    except Exception as e:
        result["error"] = str(e)
        print(f"[X] 失败: {e}")

    return result


# ============================================================
# 4. 结果统计
# ============================================================


def generate_summary(results):
    """生成扫描摘要"""
    total = len(results)
    success = sum(1 for r in results if r["status"] is not None)
    status_200 = sum(1 for r in results if r["status"] == 200)
    status_403 = sum(1 for r in results if r["status"] == 403)
    error = sum(1 for r in results if r["error"])

    return {
        "total_targets": total,
        "reachable": success,
        "200_ok": status_200,
        "403_forbidden": status_403,
        "errors": error,
    }


# ============================================================
# 5. 保存报告
# ============================================================


def save_report(results, filepath):
    """保存 JSON 报告"""
    summary = generate_summary(results)
    report = {
        "scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary,
        "results": results,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n[+] 报告已保存到 {filepath}")


# ============================================================
# 6. 主程序入口
# ============================================================


def main():
    """主函数 — 你以后写的每个安全工具都是这个结构"""
    print("=" * 50)
    print("  WebInfo — 简易信息收集工具 v0.1")
    print("=" * 50)

    # 解析参数
    args = parse_args()

    # 如果没有提供目标文件，交互式输入
    if args["target_file"] is None:
        args["target_file"] = input("\n目标文件路径: ").strip()
        args["output"] = input("报告输出路径 (默认 report.json): ").strip() or "report.json"

    print(f"\n目标文件: {args['target_file']}")
    print(f"输出文件: {args['output']}")
    print(f"超时时间: {args['timeout']}s\n")

    # 加载目标
    urls = load_urls(args["target_file"])

    # 创建示例文件（如果目标文件不存在的话）
    if not Path(args["target_file"]).exists():
        sample = """# 测试目标列表
httpbin.org
www.baidu.com
192.168.1.1:8080
http://example.com/admin
http://testphp.vulnweb.com"""
        with open(args["target_file"], "w", encoding="utf-8") as f:
            f.write(sample)
        print(f"[+] 已创建示例目标文件: {args['target_file']}")
        urls = load_urls(args["target_file"])

    if not urls:
        print("[!] 没有可扫描的目标")
        return

    # 逐个探测
    print(f"开始探测 {len(urls)} 个目标...\n")
    results = []
    for i, url in enumerate(urls, 1):
        result = probe_url(url, timeout=args["timeout"])
        results.append(result)

    # 保存报告
    save_report(results, args["output"])

    # 打印摘要
    summary = generate_summary(results)
    print(f"\n{'=' * 50}")
    print("扫描摘要")
    print(f"{'=' * 50}")
    for k, v in summary.items():
        print(f"  {k}: {v}")


# Python 程序入口（相当于 C 的 int main()）
if __name__ == "__main__":
    main()
