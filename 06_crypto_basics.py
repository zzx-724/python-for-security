"""
Day 6: 密码学 Python 入门 — 你的专业主场
安全场景：哈希计算、Base64编解码、简单加解密、CTF 密码题

作为密码科学与技术专业的学生，这一课是你的"专业武器"。
Python 的密码学生态极其丰富，从哈希到公钥加密全有现成库。
"""

import hashlib
import base64
import binascii

# ============================================================
# 1. 哈希计算 — hashlib（核心！）
# ============================================================

data = "Hello, Cryptography!"

# MD5（已不安全，但 CTF 和旧系统里还有）
md5_hash = hashlib.md5(data.encode()).hexdigest()
print(f"MD5:    {md5_hash}")

# SHA1（也已不安全）
sha1_hash = hashlib.sha1(data.encode()).hexdigest()
print(f"SHA1:   {sha1_hash}")

# SHA256（目前安全）
sha256_hash = hashlib.sha256(data.encode()).hexdigest()
print(f"SHA256: {sha256_hash}")

# 分块更新（处理大文件时用，不能一次读完整个文件到内存）
hasher = hashlib.sha256()
hasher.update(b"Hello, ")       # b 前缀表示 bytes 类型
hasher.update(b"Cryptography!")
print(f"SHA256(分块): {hasher.hexdigest()}")

# ============================================================
# 2. 破解简单哈希 — 字典攻击演示
# ============================================================
print("\n--- 字典攻击演示 ---")

# 假设我们从某个数据库泄露中得到了这个哈希
target_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
print(f"目标哈希: {target_hash}")

# 常见密码字典
common_passwords = [
    "123456", "password", "admin", "12345678",
    "qwerty", "letmein", "monkey", "football",
    "iloveyou", "master", "welcome", "password1", "password",
]

print("尝试字典攻击...")
for pwd in common_passwords:
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    if pwd_hash == target_hash:
        print(f"  [+] 找到！密码是: '{pwd}'")
        break
else:
    # for-else: for 循环正常结束（没 break）才执行
    # 这是 Python 特有语法，相当于"没找到"的情况
    print("  [-] 字典中未找到")

# ============================================================
# 3. Base64 与 Hex 编解码
# ============================================================
print("\n--- 编解码工具箱 ---")

original = "管理员:Admin@123"
print(f"原始文本: {original}")

# Base64
b64 = base64.b64encode(original.encode()).decode()
print(f"Base64编码: {b64}")
print(f"Base64解码: {base64.b64decode(b64).decode()}")

# 十六进制
hex_str = original.encode().hex()
print(f"Hex编码:    {hex_str}")
print(f"Hex解码:    {bytes.fromhex(hex_str).decode()}")

# URL 安全的 Base64（把 +/ 换成 -_）
url_b64 = base64.urlsafe_b64encode(original.encode()).decode()
print(f"URL-Base64: {url_b64}")

# ============================================================
# 4. 经典密码 — 凯撒密码、异或加密
# ============================================================
print("\n--- 经典密码 ---")


def caesar_encrypt(text, shift):
    """凯撒密码加密"""
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
        else:
            result += char
    return result


def caesar_decrypt(text, shift):
    """凯撒密码解密 = 用 -shift 加密"""
    return caesar_encrypt(text, -shift)


plaintext = "HELLO WORLD"
ciphertext = caesar_encrypt(plaintext, 3)
decrypted = caesar_decrypt(ciphertext, 3)

print(f"原文:   {plaintext}")
print(f"凯撒+3: {ciphertext}")
print(f"解密:   {decrypted}")


def xor_cipher(data, key):
    """异或加解密（加解密是同一个操作）"""
    key_bytes = key.encode() if isinstance(key, str) else key
    result = bytearray()
    for i, byte in enumerate(data.encode() if isinstance(data, str) else data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)


# 异或加密演示
msg = "Secret Message"
key = "XORKEY"
encrypted = xor_cipher(msg, key)
decrypted = xor_cipher(encrypted, key)

print(f"\n原文:      {msg}")
print(f"异或加密:  {encrypted.hex()}")
print(f"异或解密:  {decrypted.decode()}")

# ============================================================
# 5. CTF 常见编码转换工具函数
# ============================================================
print("\n--- CTF 编码工具箱 ---")


def decode_auto(data):
    """尝试自动识别并解码常见的 CTF 编码"""
    data = data.strip()
    results = {}

    # 尝试 Hex
    try:
        decoded = bytes.fromhex(data).decode("utf-8")
        results["hex"] = decoded
    except (ValueError, UnicodeDecodeError):
        pass

    # 尝试 Base64
    try:
        decoded = base64.b64decode(data).decode("utf-8")
        results["base64"] = decoded
    except (Exception,):
        pass

    # 尝试 Base64 URL-safe
    try:
        decoded = base64.urlsafe_b64decode(data + "=" * (4 - len(data) % 4)).decode("utf-8")
        results["b64url"] = decoded
    except (Exception,):
        pass

    return results


# 测试自动解码
test_encoded = base64.b64encode(b"flag{python_is_fun}").decode()
print(f"输入: {test_encoded}")
print(f"自动解码: {decode_auto(test_encoded)}")

# ============================================================
# 6. 练习
# ============================================================
print("\n--- 练习 ---")
print("1. 写一个函数，计算给定字符串的所有常见哈希 (MD5, SHA1, SHA256, SHA512)")
print("2. 写一个凯撒密码暴力破解函数，尝试 1-25 所有偏移量")
print("3. 找一个 CTF 密码题，用 Python 写脚本解出来")
print("   推荐 BUUCTF Crypto 分类 → https://buuoj.cn/challenges")
