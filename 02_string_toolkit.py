"""
Day 2: 字符串操作 — 安全人员的"瑞士军刀"
安全场景：处理 URL、Payload 拼接、编码解码、正则提取

Python 的字符串是安全脚本里用得最频繁的东西，
URL 拼接、Payload 生成、Base64 解码、正则匹配全靠它。
"""

import base64  # Python 自带的 Base64 库

# ============================================================
# 1. 字符串切片 — 提取子串，安全日志分析的基础
# ============================================================
url = "http://target.com/admin/login.php"
print("原始 URL:", url)

# 提取协议
protocol = url[:4]  # 前 4 个字符 → "http"
print("协议:", protocol)

# 提取域名
# 找到 "//" 之后、下一个 "/" 之前
start = url.index("//") + 2  # index() 返回首次出现位置
end = url.index("/", start)
print("start =",start,"end =",end)
domain = url[start:end]
print("域名:", domain)

# 提取路径
path = url[end:]
print("路径:", path)

# 反转字符串（检查回文域名用）
print("反转:", url[::-1])

# ============================================================
# 2. 字符串方法大全 — 安全脚本常用
# ============================================================
print("\n--- 字符串方法 ---")

# split — 拆分 URL 路径
path_parts = "/admin/login.php".split("/")
print("路径拆分:", path_parts)  # ['', 'admin', 'login.php']

# join — 拼接路径
rebuilt = "/".join(["", "admin", "config.php"])
print("路径拼接:", rebuilt)  # /admin/config.php

# replace — Payload 中替换占位符
payload_template = "SELECT * FROM users WHERE id = '{ID}'"
payload = payload_template.replace("{ID}", "1 OR 1=1")
print("Payload 生成:", payload)

# strip — 去掉响应中的空白字符（扫描结果经常有空格换行）
response = "  200 OK\n"
clean_response = response.strip()
print(f"原始响应: '{response}'")
print(f"清理后:   '{clean_response}'")

# upper/lower — SQL 注入中大小写绕过
sql = "Union Select Password From Users"
print("全大写绕过:", sql.upper())
print("全小写绕过:", sql.lower())

# startswith/endswith — 判断 URL 特征
malicious_url = "http://evil.com/malware.exe"
print(f"是 HTTPS 吗？{malicious_url.startswith('https://')}")  # False
print(f"是 .exe 吗？{malicious_url.endswith('.exe')}")          # True

# find — 在响应中定位关键词
html = '<html><head><title>Admin Panel</title></head></html>'
title_start = html.find("<title>") + len("<title>")
title_end = html.find("</title>")
print("提取标题:", html[title_start:title_end])

# ============================================================
# 3. 编码解码 — 密码学/Web安全必备
# ============================================================
print("\n--- 编码解码 ---")

# 字符串 ↔ 字节（编码）
text = "admin"
bytes_data = text.encode("utf-8")  # 字符串 → 字节
print(f"'{text}' → 字节: {bytes_data}")
print(f"字节 → 字符串: {bytes_data.decode('utf-8')}")

# Base64 编码解码
original = "admin:password123"
encoded = base64.b64encode(original.encode()).decode()
decoded = base64.b64decode(encoded).decode()
print(f"\n原始: {original}")
print(f"Base64: {encoded}")
print(f"解码: {decoded}")

# 十六进制
text_cn = "你好"
hex_str = text_cn.encode("utf-8").hex()
print(f"\n'你好' 的十六进制: {hex_str}")
print(f"十六进制还原: {bytes.fromhex(hex_str).decode('utf-8')}")

# ============================================================
# 4. 练习：字符串综合实战（只用你学过的知识）
# ============================================================
print("\n--- 练习: URL 解析 + Payload 生成 ---")

# ------------------------------------------------------------
# 练习 A：从 URL 里提取查询参数
# ------------------------------------------------------------
# 场景：渗透测试时，要从 URL 里扒出参数名和值，才能知道往哪里注入
url = "http://target.com/search?q=admin&page=2&debug=1"

query = url[url.find("?") + 1:]
print(f"{query}")

params = query.split("&")
print(f"{params}")

first = params[0]
name = first.split("=")[0]
value = first.split("=")[1]
print(f"第一个值: {name} = {value}")
#-------------------------------------------------------------------------------------------------------------
# 步骤 1：用 find 找到 "?" 的位置，切片取出它后面的内容
#   提示：url[位置+1:]  从该位置之后一直取到结尾
#   预期：q=admin&page=2&debug=1
query = url[url.find("?") + 1:]
print("查询字符串:", query)

# 步骤 2：用 split("&") 把参数拆成列表
#   预期：['q=admin', 'page=2', 'debug=1']
params = query.split("&")
print("参数列表:", params)

# 步骤 3：取第一个参数（索引 0），用 split("=") 拆出参数名和值
#   预期：参数名 q，值 admin
first = params[0]
name = first.split("=")[0]
value = first.split("=")[1]
print(f"第一个参数: {name} = {value}")
# ------------------------------------------------------------
# 练习 B：Payload 模板生成器（只用 replace，不用函数）
# ------------------------------------------------------------
# 场景：往 URL 参数里塞各种测试 Payload，看服务器什么反应
url_template = "http://target.com/search?q={PAYLOAD}"

# 任务：用 replace 生成下面 3 个测试 URL 并打印
#   1. payload = "test"                      普通测试，看页面正不正常
#   2. payload = "' OR 1=1-- -"              SQL 注入探测
#   3. payload = "<script>alert(1)</script>" XSS 探测
#   提示：url_template.replace("{PAYLOAD}", payload)

# === 你的代码写在这里 ===
payload1 = url_template.replace("{PAYLOAD}","test")
print(payload1)
payload2 = url_template.replace("{PAYLOAD}","' OR 1=1-- -")
print(payload2)
payload3 = url_template.replace("{PAYLOAD}","<script>alert(1)</script>")
print(payload3)

# ------------------------------------------------------------
# 练习 C：清理响应 + 判断结果（strip + if/elif/else 复习）
# ------------------------------------------------------------
# 场景：扫描器拿到服务器响应，判断这个页面到底存不存在
response = "  200 OK\n"   # 注意：前后有空格，末尾有换行！

# 任务：
#   1. 用 strip() 清洗掉首尾的空格和换行
#   2. 用 startswith("200") 判断是不是成功响应
#   3. 用 if/else 打印 "✅ 页面存在" 或 "❌ 页面不存在"
# 提示：洗完之后再用 startswith 判断，否则永远不匹配

# === 你的代码写在这里 ===
clean_response = response.strip()
print(f"是否响应成功?{clean_response.startswith('200')}")
if clean_response.startswith('200'):
    print("✅ 页面存在")
else:
    print("❌ 页面不存在")

# ------------------------------------------------------------
# 挑战题（选做）：WAF 大小写绕过
# ------------------------------------------------------------
# 场景：很多 WAF 只匹配小写的 "union select"，把关键字混着大小写写就能绕过
# 任务：把下面这句 Payload 变成 "UnIoN SeLeCt" 这种混合大小写的形式
sql = "union select password from users"
# 提示：这时候 upper() 全大写、lower() 全小写都不好使
#      可以试试切片取一部分 + upper()/lower() 拼起来
#      比如 sql[:5].upper() + sql[5:12].lower() + ...

# === 你的代码写在这里 ===
one = sql[:5].upper()
two = sql[5:12].lower()
three = sql[12:len(sql)].upper()
new_sql = one + two + three
print(new_sql)
# ============================================================
# ⛔ 以下内容超纲，先跳过！等学到 Day 3（字典）和 Day 5（函数）再回来看
# ============================================================
# 这是本来的练习题，用到了你还没学的：函数 def、字典 {}、列表推导式。
# 现在看不懂很正常，完全不用管，学到相应内容再回来：
#
# def generate_sqli_payload(method, column_count):
#     methods = {
#         "union": f"' UNION SELECT {', '.join(['NULL'] * column_count)}-- -",
#         "error": f"' AND extractvalue(1,concat(0x7e,({'+'.join(['NULL'] * column_count)})))-- -",
#     }
#     return methods.get(method, "Unknown method")
#
# payload = generate_sqli_payload("union", 5)
# print("UNION Payload:", payload)
