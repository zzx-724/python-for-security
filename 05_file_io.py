"""
Day 5: 函数 + 文件读写 + 异常处理 — 把脚本变成工具
安全场景：读取目标列表文件、保存扫描报告、命令行参数、错误处理

一个真正的安全工具需要：
1. 函数封装（复用代码）
2. 文件读写（读目标、写报告）
3. 异常处理（网络超时、文件不存在）
"""

import json
import sys
from pathlib import Path  # Python 3.4+ 推荐的路径处理方式

# ============================================================
# 1. 函数 — 封装复用逻辑
# ============================================================

# 基础函数（和 C 差不多，但参数更灵活）


def scan_port(ip, port, timeout=3):
    """
    模拟端口扫描
    timeout 有默认值 3，调用方可以不传
    """
    # 实际扫描用 socket，这里先模拟
    print(f"    扫描 {ip}:{port} (超时={timeout}s) ... ", end="")
    # 返回格式：(端口, 状态, 服务名)
    known_services = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
    import random
    if random.random() < 0.3:
        service = known_services.get(port, "unknown")
        print("OPEN")
        return {"port": port, "status": "open", "service": service}
    else:
        print("closed")
        return {"port": port, "status": "closed", "service": None}


# 扫描单个 IP 的所有端口 — 一个函数调用另一个函数
def scan_host(ip, port_list):
    """扫描一个 IP 的所有端口，返回结果列表"""
    results = []
    for p in port_list:
        result = scan_port(ip, p)  # 调用上面的函数
        results.append(result)
    return results


# 测试
print("--- 扫描测试 ---")
results = scan_host("192.168.1.1", [22, 80, 443])
open_ports = [r for r in results if r["status"] == "open"]
print(f"  开放端口: {open_ports}")

# ============================================================
# 2. 文件读写 — 读目标列表，写扫描报告
# ============================================================

# 先创建示例目标文件
target_list = """# 目标列表（#开头的是注释行）
192.168.1.1
192.168.1.2
192.168.1.3
10.0.0.1
"""

# 写入示例文件
with open("targets.txt", "w", encoding="utf-8") as f:
    f.write(target_list)
print("\n[+] 示例文件 targets.txt 已创建")


def load_targets(filepath):
    """从文件加载目标列表，跳过注释和空行"""
    targets = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()  # 去掉首尾空白
                if line and not line.startswith("#"):  # 非空且非注释
                    targets.append(line)
        print(f"[+] 从 {filepath} 加载了 {len(targets)} 个目标")
    except FileNotFoundError:
        print(f"[!] 文件 {filepath} 不存在")
        return []
    return targets


def save_report(results, filepath):
    """把扫描结果保存为 JSON 报告"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[+] 报告已保存到 {filepath}")
    except Exception as e:
        print(f"[!] 保存失败: {e}")


# 测试
targets = load_targets("targets.txt")
print(f"目标列表: {targets}")

# 模拟扫描并保存报告
dummy_report = [
    {"ip": "192.168.1.1", "open_ports": [22, 80, 443], "os": "Linux"},
    {"ip": "192.168.1.2", "open_ports": [22, 3306], "os": "Linux"},
    {"ip": "192.168.1.3", "open_ports": [80], "os": "Windows"},
]
save_report(dummy_report, "scan_report.json")

# ============================================================
# 3. 路径处理 — pathlib（别再用字符串拼路径！）
# ============================================================
print("\n--- Path 用法 ---")

report_path = Path("scan_report.json")
print(f"文件名: {report_path.name}")
print(f"后缀: {report_path.suffix}")
print(f"绝对路径: {report_path.resolve()}")
print(f"是否存在: {report_path.exists()}")
print(f"文件大小: {report_path.stat().st_size} bytes")

# 拼接路径（跨平台，Windows 和 Linux 都行）
wordlist_dir = Path("wordlists")
dir_file = wordlist_dir / "common.txt"  # / 运算符拼接路径！
print(f"字典路径: {dir_file}")

# ============================================================
# 4. 异常处理 — 安全脚本必须健壮
# ============================================================
print("\n--- 异常处理 ---")


def safe_scan(ip, port):
    """带异常保护的扫描——网络请求总会出各种意外"""
    try:
        # 模拟扫描，有可能"网络超时"
        import random
        if random.random() < 0.1:
            raise ConnectionError("网络超时")

        result = scan_port(ip, port)
        return result
    except ConnectionError as e:
        print(f"    [!] {ip}:{port} 连接失败: {e}")
        return {"port": port, "status": "error", "error": str(e)}
    except Exception as e:
        print(f"    [!] 未知错误: {e}")
        return {"port": port, "status": "error", "error": str(e)}


# 测试异常保护
print("安全扫描（带异常保护）:")
safe_scan("192.168.1.1", 80)

# ============================================================
# 5. 练习：完整的扫描脚本骨架
# ============================================================
print("\n--- 练习 ---")
print("""
试试把这些函数组合成一个完整的扫描小工具：
1. load_targets() 读取目标列表
2. 循环调用 safe_scan() 扫描每个目标的常用端口
3. save_report() 把结果保存为 JSON
4. 添加 try/except 保护所有可能出错的地方

提示：把上面的代码复制到新文件，加上你的逻辑即可。
""")
