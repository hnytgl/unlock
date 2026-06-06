# unlock

终端编码解码与加解密工具箱。

在终端中快速完成编码转换、哈希计算、古典密码加解密操作，无需打开浏览器或 GUI 工具。

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
# 查看所有命令
python unlock.py

# 编码/解码
python unlock.py url "你好世界"
python unlock.py b64 "SGVsbG8="
python unlock.py hexc "你好"
python unlock.py info "hello world"

# 哈希
python unlock.py md5 "hello"
python unlock.py sha256 "hello"
python unlock.py ntlm "hello"
python unlock.py all "hello"

# 古典密码
python unlock.py caesar "hello" 3
python unlock.py caesarx "KroDv"        # 暴力破解
python unlock.py rot13 "hello"
python unlock.py morse "hello world"
python unlock.py vig "hello" "key"
python unlock.py adfgx "hello" "key"    # 需 pycipher
python unlock.py xor "hello" "key"

# 交互模式
python unlock.py interact
```

## 功能列表

### 编码/解码

| 命令 | 说明 |
|------|------|
| `url` | URL 编码 |
| `urld` | URL 解码 |
| `b64` | Base64 编码 |
| `b64d` | Base64 解码 |
| `b64u` | URL-safe Base64 编码 |
| `b64ud` | URL-safe Base64 解码 |
| `hex` | 字符串 → 十六进制 |
| `hexd` | 十六进制 → 字符串 |
| `html` | HTML 实体编码 |
| `htmld` | HTML 实体解码 |
| `uni` | 中文 → Unicode 转义 |
| `unid` | Unicode 转义 → 中文 |
| `hexc` | 中文 → 十六进制 (UTF-8 + GBK) |
| `bin` | 字符串 → 二进制 |
| `oct` | 字符串 → 八进制 |
| `dec` | 字符串 → 十进制 |
| `bind` | 二进制 → 字符串 |
| `octd` | 八进制 → 字符串 |
| `decd` | 十进制 → 字符串 |
| `rev` | 字符串反转 |
| `info` | 字符串统计信息 |
| `ip2i` | IP → 整数 |
| `i2ip` | 整数 → IP |

### 哈希

| 命令 | 说明 |
|------|------|
| `md5` | MD5 (32位+16位) |
| `sha256` | SHA-256 |
| `ntlm` | NTLM Hash |
| `all` | 全部 (MD5/SHA1/256/512/SHA3/BLAKE2/NTLM) |

### 加密/解密

| 命令 | 说明 |
|------|------|
| `caesar` | 凯撒加密 |
| `caesard` | 凯撒解密 |
| `caesarx` | 凯撒暴力破解 (1-25) |
| `rot13` | ROT13 |
| `rot47` | ROT47 |
| `atbash` | Atbash 密码 |
| `vig` / `vigd` | 维吉尼亚加密/解密 |
| `morse` / `morsed` | 摩斯电码编码/解码 |
| `bacon` / `bacond` | 培根密码 |
| `fence` | 栅栏密码 |
| `adfgx` / `adfgxd` | ADFGX 加密/解密 |
| `adfgvx` / `adfgvxd` | ADFGVX 加密/解密 |
| `xor` / `xord` | XOR 加解密 |

## 交互模式

```bash
python unlock.py interact
```

进入交互式 shell，直接输入命令即可：

```
unlock> md5 hello
unlock> b64 SGVsbG8=
unlock> caesar hello 3
unlock> exit
```

## 相比原版的变化

- **Python 3.x 迁移** — 原版仅支持 Python 2.7
- **模块化架构** — 编码/哈希/密码学分离
- **argparse CLI** — 统一的参数解析
- **交互模式** — 方便快速操作
- **新增功能** — ROT13/47、XOR、进制转换、IP 转换、字符串统计、SHA3、BLAKE2、NTLM 等
- **统一输出** — 有颜色的格式化结果
- **错误处理** — 缺失参数友好提示
- **无需 pycipher** — 基础功能独立可用（仅 ADFGX/ADFGVX 需要）

## 免责声明

仅供授权的安全评估与学习研究使用。
