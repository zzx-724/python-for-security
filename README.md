# python-for-security

密码科学与技术专业 · 网络安全方向的 Python 学习记录。

从零基础开始，每天 1-2 小时，所有练习代码和进度都记录在这个仓库里。

## 背景

- **专业**：密码科学与技术
- **已有基础**：C 语言学完语法，Python 从零开始
- **学习方向**：网络安全 → 渗透测试脚本 / 密码学编程 / 安全自动化
- **开始时间**：2026-09-10

## 学习路线

```
阶段一（9 天）        阶段二（4 周）           阶段三（长期）
Python 语法速通      安全方向 Python 工具箱    实战项目积累
基础 + 密码学小练习   网络/Web/系统/加密       端口扫描器/爆破器
                                              /CTF自动化/WAF绕过
```

## 目录结构

```
.
├── 01_first_steps.py             # Day 1  变量、类型、print/input、f-string
├── practice_01.py                # Day 1  练习：端口服务识别器（if/elif/else）
├── 02_string_toolkit.py          # Day 2  字符串操作、编码解码、Payload 生成
├── 03_data_structures.py         # Day 3  列表、元组、字典、集合
├── 04_scanning_logic.py          # Day 4  循环、推导式、enumerate/zip
├── practice_02_enumerate_zip.py  # Day 4  专项练习：enumerate 与 zip
├── 05_functions.py               # Day 5  函数、参数、作用域、return vs print
├── 06_file_io.py                 # Day 6  文件读写、JSON
├── 07_exception_handling.py      # Day 7  异常处理 try/except
├── 08_oop.py                     # Day 8  面向对象 class / self / 属性 / 方法
├── 09_info_gather.py             # Day 9  综合项目：简易信息收集工具（参考实现）
├── project_01_log_analyzer.py    # 项目 01 访问日志分析器（Day 6-7 交付）
├── bonus_crypto_basics.py        # 加餐  哈希、Base64、凯撒、异或、CTF 编码
├── MISTAKES.md                   # 真实踩过的坑，写代码前扫一眼
├── CHEATSHEET.md                 # 语法速查表
├── PYTHON_LEARNING_PLAN.md       # 完整学习计划与进度追踪
└── access.log / bad_access.log   # 练习用日志数据
```

**命名规则：** `NN_主题.py`，`NN` 就是 Day 编号。
`practice_*` 是当天专项练习，`project_*` 是正式项目，`bonus_*` 是加餐专题。

## 学习进度

| 阶段 | 内容 | 状态 |
|------|------|:--:|
| Day 1 | 变量、类型、print/input、条件判断 | ✅ |
| Day 2 | 字符串操作、切片、编码解码 | ✅ |
| Day 3 | 列表、元组、字典、集合 | ✅ |
| Day 4 | 循环、推导式、enumerate/zip | ✅ |
| Day 5 | 函数、参数、作用域、return vs print | ✅ |
| Day 6 | 文件读写、JSON | ✅ |
| Day 7 | 异常处理 try/except | ✅ |
| 项目 01 | 访问日志分析器（可容错版本） | ✅ |
| Day 8 | 面向对象 class / self / 属性 / 方法 | ⬜ |
| Day 9 | 阶段一综合项目：信息收集工具 | ⬜ |

详细进度、每个知识点的笔记和踩过的坑，见 [PYTHON_LEARNING_PLAN.md](PYTHON_LEARNING_PLAN.md)。

## 环境

- Python 3.14.5
- VS Code
- Windows 11

## 运行方式

```bash
# 克隆
git clone <repo-url>
cd python-for-security

# 运行任意一天的练习
python 01_first_steps.py
```

部分脚本含 `input()` 交互输入，请在终端运行（VS Code 按 `Ctrl+F5`）。

## 说明

代码为学习过程记录，按教学顺序编排，脚本中保留了大量中文注释，记录知识点、C 语言对比和踩过的坑。后续会随着学习推进持续更新，并进入阶段二的实战项目（端口扫描器、目录爆破器、加解密工具箱等）。
