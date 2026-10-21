# 犯错记录 —— 我真实踩过的坑

> 这份不是"错误大全"，是我自己在 Day 6 和项目 01 里**真实犯过**的错。
> 每一条都有代码、有原因、有正确写法。
>
> **用法：每次写代码前扫一眼。** 这些不是"粗心"，是反复出现的思维习惯。

---

## 一、缩进 = 作用域（Python 最致命的一类错）

Python 没有大括号，**一行代码属于哪一层，完全看缩进。**

### 1. `if` 缩进和 `for` 同级 → 只检查了最后一行

**我写的：**
```python
for line in f:
    parts = line.split()
if parts[6] in sensitive_path:      # ← 和 for 一样高，在循环【外面】
    suspects.add(parts[0])
```

**现象**：`suspects` 一直是空的，但代码不报错。

**原因**：`if` 和 `for` 平级，所以它只在循环**结束后**执行一次。
那时循环已经跑完，只有 `parts` 里的最后一行还被保留着 ——
**一行怎么可能代表 46 行日志？**

**正确：**
```python
for line in f:
    parts = line.split()
    if parts[6] in sensitive_path:   # ← 多缩进一层
        suspects.add(parts[0])
```

**教训**：不报错 ≠ 没错。**结果为空时，第一个要看的就是缩进。**

---

### 2. `print` 在循环里 → 打印了 46 次

**我写的：**
```python
for line in f:
    ...
    print(count)        # ← 缩进在循环里
```

**现象**：字典被打印了 46 次，刷满屏幕。

**正确**：要**最终结果**就退一格；要**过程**才留在循环里。

```python
for line in f:
    ...
print(count)            # ← 循环跑完才打印一次
```

**教训**：调试时打印过程是有价值的（能看见计数怎么涨起来），
但**交付前必须删掉。**

---

## 二、引号与括号的层级（我踩了 4 次）

这一类是我犯得最多的：**把该放在外面的符号，写进了引号里。**

### 3. `"ip: ip"` —— 冒号写进了引号里

**我写的：**
```python
report.append({"ip: ip", "count": n})       # ❌
```

**现象**：`不允许在 set 内使用键/值对`

**原因**：`"ip: ip"` 是一个**普通字符串**，不是键值对。
Python 看到 `{字符串, 键: 值}` 这种混合体，就把 `{}` 当成集合（set），
而集合不允许放键值对 → 报错。

**正确：**
```python
report.append({"ip": ip, "count": n})       # ✅ 冒号在引号【外面】
```

**这个错误的家族成员（我都踩过）：**
- Day 4：`[set(a) - set(b)]` —— 括号套错层
- Day 5：`{f"端口 {port}"}` —— 该是 dict 的地方写了 set
- Day 6 练习 B：`"target\n"` —— 写成了字面量 `target` 而不是变量
- Day 6 练习 D：`"ip: ip"` —— 冒号在引号里

**自查方法**：写 `{}` 时问自己 —— **里面有没有冒号？冒号在引号里还是外？**

---

## 三、函数：输入与输出

### 4. 函数偷用全局变量 → 调用两次，结果翻倍

**我写的：**
```python
count = {}                       # 全局

def count_by_ip(filepath):
    for line in f:
        count[parts[0]] += 1     # 偷用外面的 count
    return count
```

**后果**：调两次，`25` 变 `50`。

**原因**：函数应该是**黑盒** —— 给原料，出成品，中间用什么容器是自己的事。
用全局变量等于**在别人的冰箱里拿东西做菜**，上次做剩的还在里面。

**正确：**
```python
def count_by_ip(filepath):
    count = {}                   # ← 搬进函数里，每次从零开始
    ...
    return count
```

**原则**：**函数要什么，通过参数要；算出的什么，通过 `return` 交。**
不伸手去外面拿，也不偷偷往外面写。

---

### 5. `return` 的值没人接 → 结果是空的

**我写的：**
```python
def sort_counts(counts):
    ranked = sorted(...)
    return ranked

sort_counts(count)               # ❌ 递出去了，没人接
print(ranked)                    # []  ← 全局的 ranked 从没变过
```

**原因**：`return` 是把东西**递出函数**，但外面得**伸手接住**。
`ranked = sorted(...)` 在函数里是**局部变量**，函数一结束就没了。

**正确：**
```python
ranked = sort_counts(count)      # ✅ 接住
```

**规律**：**函数有 `return`，调用处就得有 `=`。**

---

### 6. `open` 和 `json.dump` 的两个参数用反了

**我写的：**
```python
def save_report(report, save_path):
    with open(report, "w", ...) as f:        # ❌ open 要地址
        json.dump(save_path, f, ...)         # ❌ dump 要数据
```

**现象**：`TypeError: expected str, bytes or os.PathLike object, not list`

**原因**：正好反了。`open` 要**路径**，`json.dump` 要**数据**。

**正确：**
```python
with open(save_path, "w", ...) as f:         # ✅
    json.dump(report, f, ...)                # ✅
```

**记法**：**先把车开进停车场（open 路径），再把行李放进后备箱（dump 数据）。**

---

## 四、数据结构选错

### 7. 用 set 计数 → 次数全丢了

**我一开始的想法**："用集合，方便操作，集合会自动去重。"

**现象**：46 条记录塌缩成 4 个 IP，**每个 IP 访问了几次，完全丢失**。

**原因**：集合只回答「**有哪些**」，不回答「**多少个**」。
而客户要的正是「**多少个**」。

**正确**：用字典 `{IP: 次数}`。

| 问题 | 用什么 |
|---|---|
| 有哪些 IP？ | set |
| 每个 IP 多少次？ | dict |
| 一堆多条记录、每条多个字段 | list of dict |

**补充**：如果非要用 set，就得对每个元素 `ips.count(ip)` ——
那是 O(n²)，46 条还行，几百万条会跑到天荒地老。

---

## 五、调试习惯

### 8. 输出不带身份信息 → 分不清哪行是谁的

**我写的：**
```python
if parts[0] == "10.0.0.99" or parts[0] == "203.0.113.7":
    print(parts[6])
```

**现象**：37 行路径混在一起，判断不出哪一行属于哪个 IP，
结果**分析结论是错的**，而且我自己没发现。

**正确：**
```python
print(parts[0], parts[6])        # 每行自带身份
```

**原则**：**日志分析里，任何一行输出都应该自带"我是谁"。**

---

### 9. 筛错了 IP，把同一份输出贴了两次

**我写的：**
```python
elif parts[0] == "192.168.1.50":   # 想筛 203.0.113.7
```

**现象**：两次贴出来的输出一模一样，我以为是"代码没生效"。

**教训**：**怀疑代码没生效之前，先检查自己筛的是不是对的东西。**
"输出没变"有两种可能：代码没跑，或者你一直在看错的对象。

---

### 10. 把三引号 `'''...'''` 当注释用

**我写的：**
```python
'''
for ip, count_1 in ranked:
    ...
'''
```

**真相**：这不是注释，**是一个字符串字面量**。
Python 会老老实实构造出这个长字符串，然后……扔掉。

它能"不报错"，但这叫**死代码**。最坑的是：
**它不会跟着重构一起更新。** 我改完参数名，里面还是旧的 `count_1`。

**正确**：真注释用 `#`；不用的代码**直接删掉**，别留着。

---

### 11. 复制粘贴导致重复执行

**我写的：**
```python
ranked = sort_counts(count)
ranked = sort_counts(count)      # ← 多粘了一行
```

**后果**：不报错，但白算两遍。

**教训**：重构时挪代码特别容易多粘一次。
**改完不要只看结果对不对，要自己扫一眼代码。**

---

### 12. 变量名遮蔽

**我写的：**
```python
count = {}                       # 字典

for ip, count in ranked:         # 循环变量也叫 count
    ...
# 循环结束后，count 变成了一个整数，字典没了
```

**后果**：这次没出事（后面没再用 `count`），
但下次在下面写 `count["10.0.0.99"]` 就会炸：
`TypeError: 'int' object is not subscriptable`

**正确**：`for ip, n in ranked:`

**同类错误**：Day 3 用 `list` 当变量名，遮住了内置函数。

---

## 六、JSON

### 13. 用 `f.write(dict)` 写字典 → 根本不是 JSON

**我写的：**
```python
def save_targets(targets, filepath):
    with open(filepath, "w", ...) as f:
        f.write(str(report))     # ❌
```

**现象**：`JSONDecodeError: Expecting property name enclosed in double quotes`

**原因**：`str(dict)` 产出的是 **Python repr**，用的是单引号：
```python
{'ip': '10.0.0.99'}       # 这不是合法 JSON
```
JSON 要求**双引号**。

**正确**：`json.dump(report, f, ensure_ascii=False, indent=2)`

---

### 14. 少了 `encoding="utf-8"` 或 `ensure_ascii=False`

**这台机器的坑**：`locale.getpreferredencoding()` 返回 **`cp936`（GBK）**。
不加 `encoding="utf-8"` 写中文，再用 UTF-8 读，直接报：
```
'utf-8' codec can't decode byte 0xb1
```

**正确写法（三件套，缺一不可）：**
```python
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

| 参数 | 不加会怎样 |
|---|---|
| `encoding="utf-8"` | 这台机器默认 GBK，中文读写错乱 |
| `ensure_ascii=False` | 中文变成 `访问...` |
| `indent=2` | 整个 JSON 挤成一行，人没法看 |

---

## 七、异常处理（Day 7）

### 15. `try` 包在了循环**外面** → 一个坏行终止整个循环

**我写的：**
```python
try:
    for port in ports:
        good.append(int(port))
except ValueError:
    ...
```

**现象**：只处理了前 2 个，遇到 `"abc"` 之后就不动了。

**原因**：异常不是“跳过这一行”，而是“**一路往外跳，跳到能接住它的 `except`**”。
`except` 在 `for` 外面，所以跳出去之后**循环已经被抛弃了**，不会回到循环。

**正确：**
```python
for port in ports:
    try:
        good.append(int(port))
    except ValueError:
        ...
```

**这个错我犯了两次**（练习 A、练习 C）。

---

### 16. `try` 太窄，包不住真正抛错的那一行

**我写的：**
```python
with open(filepath) as f:          # ← 抛 FileNotFoundError 的是这里
    for line in f:
        try:
            if line and ...:
                ...
        except FileNotFoundError:  # ← 接的是"里面"的错
            ...
```

**现象**：程序照样崩，报 `FileNotFoundError`。

**原因**：`open()` 在 `try` 的**上面**。异常从外面飞出去了，`except` 根本看不到。

**正确：** `try` 要包住 `open`。

**规律（15 和 16 是同一条）：**
> **`try` 的范围必须正好包住“会出事的那几行”。**
> 太宽 → 一个错终止全部；太窄 → 该接的接不住。

---

### 17. 只写 `try` 不写 `except`

**现象：**
```
SyntaxError: expected 'except' or 'finally' block
```

`try` 后面必须有 `except` 或 `finally`。这不是运行时错误，是**解析阶段**就拒绝了。

---

### 18. `except` 放在永远不会抛该异常的位置

```python
try:
    if line and not line.startswith("#"):   # 这里不会抛 FileNotFoundError
        report.append(line)
except FileNotFoundError:                    # ← 永远不触发
```

**Python 不会提醒你。** 不报错、不警告，那个 `except` 就永远沉默。

**这和变量名打错是同一类问题：代码能跑，但做的不是你想要的。**

---

### 19. 校验对象错了：`parts[0]` 能取到 ≠ 这行合法

**我写的：**
```python
try:
    ip = parts[0]
except IndexError:
    bad_lines += 1
```

**现象**：`garbage line` 被当成 IP 统计进去了，`bad_lines` 报 1，实际有 3 行坏的。

**原因**：我只检查了“**我能不能取到 `parts[0]`**”。
`"garbage line".split()` 有 2 段，`parts[0] = "garbage"` —— 取得到，所以“通过”了。

更阴险的：`192.168.1.77 - - [13/Oct/2026`（截断行）取到的 `parts[0]` 是个**真实的 IP**，
统计结果看起来完全正确，**但它是坏数据，而且永远不会暴露。**

**正确：** 检查**整行的结构**，而不是你恰好用到的那一格。

```python
parts = line.split()
if len(parts) < 7:          # 我要用 parts[6]，就必须至少有 7 段
    bad_lines += 1
    continue
```

**规则：需要第 N 格 → 要求至少 N+1 段。**

**两种判断的分工：**
| 写法 | 表达的意思 |
|---|---|
| `if len(parts) < 7` | “我知道这行该长什么样” —— 明确、可读 |
| `except IndexError` | “我试了，炸了” —— 兜底，但看不出期望 |

**先 `len` 检查，再 `try` 兜底。** 生产代码里两道都留。

---

### 20. 函数依赖外部变量：`len(raw_ports)` 而不是 `len(ports)`

**我写的：**
```python
def read_ports(ports):
    ...
    print(f"成功率: {len(good) / len(raw_ports) * 100 :.2f}%")
#                                ^^^^^^^^^ 外面的变量
```

**后果**：`read_ports(["22", "abc"])` 会算出 `1/8 = 12.50%`，正确是 `50.00%`。

**原因**：`raw_ports` 永远是文件顶部那 8 个，跟这次传进来什么无关。

**同一类错误在 `count_by_ip` 里也犯过**（用全局 `count` 当容器）。

**正确：** **函数只认参数。** 外面叫什么、有几个，一概不该关心。

---

### 21. `except` 里忘了 `return`，后面用了未赋值的变量

**我写的：**
```python
try:
    count, bad_lines = count_by_ip(LOG_FILE)   # ← 这里抛 FileNotFoundError
except FileNotFoundError as e:
    print("拿不到文件")
    # ← 少了 return
ranked = sort_counts(count)                    # count 从没被赋值
```

**现象：**
```
UnboundLocalError: cannot access local variable 'count'
```

**本意是“友好地停下”，结果换了个错误方式崩。**

**正确：** `except` 块的最后加 `return`，干净地结束函数。

---

## 跑代码前的 6 条自查

写完之后，逐条问自己：

1. **缩进**：`if` / `print` 到底该在循环里还是循环外？
2. **引号层级**：`{}` 里的冒号在引号外面吗？
3. **函数边界**：函数里有没有用到外面的变量？`return` 有没有人接？
4. **参数顺序**：`open` 给的是路径吗？`dump` 给的是数据吗？
5. **数据结构**：我要的是"有哪些"（set）还是"多少个"（dict）还是"多条记录"（list of dict）？
6. **输出身份**：我打印的每一行，能不能看出它属于谁？
7. **`try` 的位置**：它包住的是"会抛错的那一行"吗？在循环里还是循环外？
8. **校验对象**：我检查的是"整行的结构"，还是"我刚好用到的那一格"？

---

## 一句话总结

> 我犯的错，**几乎都不是"不会"，而是"放错位置"**。
> 缩进位置、引号位置、冒号位置、参数位置、代码块位置。
> Python 的规则很宽容，但**位置错了它不一定报错 —— 它只是默默给你一个错的结果。**
