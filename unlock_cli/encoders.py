#!/usr/bin/env python3
"""编码/解码模块 — URL, Base64, HTML, Hex, Unicode, 进制转换等。"""

import base64
import binascii
import hashlib
import html
import socket
import struct
import urllib.parse


# ── URL ─────────────────────────────────────────────────────────────────────

def url_encode(s):
    return urllib.parse.quote(s, safe="")


def url_decode(s):
    return urllib.parse.unquote(s)


def url_encode_component(s):
    """RFC 3986 风格的 URL 编码（保留更多字符）。"""
    return urllib.parse.quote(s, safe="~()*!.'")


# ── Base64 ──────────────────────────────────────────────────────────────────

def b64_encode(s):
    return base64.b64encode(s.encode()).decode()


def b64_decode(s):
    try:
        return base64.b64decode(s).decode()
    except Exception:
        return base64.b64decode(s).hex()


def b64_urlsafe_encode(s):
    return base64.urlsafe_b64encode(s.encode()).decode()


def b64_urlsafe_decode(s):
    try:
        return base64.urlsafe_b64decode(s).decode()
    except Exception:
        return base64.urlsafe_b64decode(s).hex()


# ── Hex ─────────────────────────────────────────────────────────────────────

def str_to_hex(s, encoding="utf-8"):
    return s.encode(encoding).hex()


def hex_to_str(h, encoding="utf-8"):
    try:
        return bytes.fromhex(h).decode(encoding)
    except UnicodeDecodeError:
        return bytes.fromhex(h).hex()


# ── Unicode ─────────────────────────────────────────────────────────────────

def unicode_encode(s):
    """中文 → unicode 转义序列 \\uXXXX"""
    return s.encode("unicode-escape").decode("ascii")


def unicode_decode(s):
    """unicode 转义序列 → 中文"""
    try:
        return s.encode("ascii").decode("unicode-escape")
    except Exception:
        return s.encode("latin-1").decode("unicode-escape")


# ── HTML ────────────────────────────────────────────────────────────────────

def html_encode(s):
    return html.escape(s, quote=True)


def html_decode(s):
    return html.unescape(s)


# ── Hex to Chinese (GBK / UTF-8) ───────────────────────────────────────────

def chinese_to_hex_utf8(s):
    return s.encode("utf-8").hex()


def chinese_to_hex_gbk(s):
    return s.encode("gbk").hex()


def hex_to_chinese(h, encoding="utf-8"):
    return bytes.fromhex(h).decode(encoding)


# ── 进制转换 ────────────────────────────────────────────────────────────────

def to_binary(s):
    """字符串 → 二进制表示（空格分隔）。"""
    return " ".join(format(b, "08b") for b in s.encode())


def to_octal(s):
    """字符串 → 八进制表示（空格分隔）。"""
    return " ".join(format(b, "03o") for b in s.encode())


def to_decimal(s):
    """字符串 → 十进制数组。"""
    return " ".join(str(b) for b in s.encode())


def from_binary(bin_str):
    """二进制 → 字符串。"""
    parts = bin_str.strip().split()
    return bytes(int(p, 2) for p in parts).decode(errors="replace")


def from_octal(oct_str):
    """八进制 → 字符串。"""
    parts = oct_str.strip().split()
    return bytes(int(p, 8) for p in parts).decode(errors="replace")


def from_decimal(dec_str):
    """十进制 → 字符串。"""
    parts = dec_str.strip().split()
    return bytes(int(p) for p in parts).decode(errors="replace")


# ── IP 转换 ─────────────────────────────────────────────────────────────────

def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def int_to_ip(n):
    return socket.inet_ntoa(struct.pack("!I", n))


# ── 字符串反转 ──────────────────────────────────────────────────────────────

def str_reverse(s):
    return s[::-1]


# ── 字符串长度 / 统计 ──────────────────────────────────────────────────────

def str_info(s):
    return {
        "length": len(s),
        "chars": len(s),
        "bytes": len(s.encode("utf-8")),
        "words": len(s.split()) if s.strip() else 0,
        "digits": sum(c.isdigit() for c in s),
        "letters": sum(c.isalpha() for c in s),
    }
