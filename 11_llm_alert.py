"""
Day 11（支线）：给日志告警加 AI 解释

流程：
  final_report.json  →  每条告警调用 DeepSeek  →  生成中文解释  →  llm_report.json

这对应项目要求里的「信息提取 + 内容生成」：
  - 信息提取：从日志里提取出可疑 IP、次数、原因
  - 内容生成：让模型把结构化告警翻译成人能读的风险说明

⚠️ 密钥从环境变量读，不写死在代码里，也不提交到 Git。
"""

import json
import os

import requests

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
INPUT_FILE = "final_report.json"
OUTPUT_FILE = "llm_report.json"


def get_api_key():
    """从环境变量取密钥。取不到就明确告诉用户怎么设置。"""
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise SystemExit(
            "未找到 DEEPSEEK_API_KEY。\n"
            "Git Bash:    export DEEPSEEK_API_KEY=sk-你的密钥\n"
            'PowerShell:  $env:DEEPSEEK_API_KEY="sk-你的密钥"'
        )
    return key


def explain_alert(alert, api_key):
    """把一条告警交给模型，返回一段中文解释。"""
    prompt = (
        "你是一名网络安全分析师。下面是一条访问日志告警：\n"
        f"- IP：{alert['ip']}\n"
        f"- 访问次数：{alert['count']}\n"
        f"- 触发原因：{alert['reason']}\n\n"
        "请用两句话回答：\n"
        "第一句：判断这可能是哪种行为（正常业务 / 扫描 / 爆破 / 异常访问）。\n"
        "第二句：建议怎么处置。\n"
        "不要输出多余内容。"
    )

    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=30,
    )

    # 状态码不是 2xx 时抛异常，比手动判断更清楚
    resp.raise_for_status()

    # 返回结构：{"choices": [{"message": {"content": "..."}}]}
    return resp.json()["choices"][0]["message"]["content"].strip()


def main():
    api_key = get_api_key()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        alerts = json.load(f)

    if not alerts:
        print("[!] 报告里没有告警")
        return

    print(f"[+] 读到 {len(alerts)} 条告警，开始分析\n")

    results = []
    for alert in alerts:
        print(f"[*] {alert['ip']}（{alert['reason']}）")
        try:
            explanation = explain_alert(alert, api_key)
        except requests.RequestException as e:
            print(f"    [X] 调用失败: {e}\n")
            continue

        print(f"    {explanation}\n")
        results.append({**alert, "explanation": explanation})

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[+] 已保存 {len(results)} 条到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
