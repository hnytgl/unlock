#!/usr/bin/env python3
"""加密/解密模块 — 古典密码与现代编码。"""

import re

from .utils import color

# ── Caesar / ROT ────────────────────────────────────────────────────────────

def caesar_encrypt(text, shift):
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr((ord(c) - 97 + shift) % 26 + 97))
        elif "A" <= c <= "Z":
            result.append(chr((ord(c) - 65 + shift) % 26 + 65))
        else:
            result.append(c)
    return "".join(result)


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def caesar_bruteforce(text):
    """返回所有 25 种可能的 Caesar 偏移结果。"""
    return {shift: caesar_decrypt(text, shift) for shift in range(1, 26)}


def rot13(text):
    return caesar_encrypt(text, 13)


def rot47(text):
    result = []
    for c in text:
        o = ord(c)
        if 33 <= o <= 126:
            result.append(chr(33 + (o - 33 + 47) % 94))
        else:
            result.append(c)
    return "".join(result)


# ── Atbash ──────────────────────────────────────────────────────────────────

def atbash(text):
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr(ord("z") - (ord(c) - ord("a"))))
        elif "A" <= c <= "Z":
            result.append(chr(ord("Z") - (ord(c) - ord("A"))))
        else:
            result.append(c)
    return "".join(result)


# ── Vigenère ────────────────────────────────────────────────────────────────

def _vigenere(text, key, encrypt=True):
    if not key.isalpha():
        raise ValueError("密钥必须为纯字母")

    key = key.upper()
    key_shifts = [ord(k) - 65 for k in key]
    result = []
    idx = 0
    direction = 1 if encrypt else -1

    for c in text:
        if "A" <= c <= "Z":
            s = (ord(c) - 65 + direction * key_shifts[idx % len(key_shifts)]) % 26
            result.append(chr(s + 65))
            idx += 1
        elif "a" <= c <= "z":
            s = (ord(c) - 97 + direction * key_shifts[idx % len(key_shifts)]) % 26
            result.append(chr(s + 97))
            idx += 1
        else:
            result.append(c)
    return "".join(result)


def vigenere_encrypt(text, key):
    return _vigenere(text, key, encrypt=True)


def vigenere_decrypt(text, key):
    return _vigenere(text, key, encrypt=False)


# ── 栅栏密码 (Rail Fence) ──────────────────────────────────────────────────

def rail_fence_decrypt(text):
    """栅栏密码：尝试所有可能的栏数。"""
    results = []
    n = len(text)
    for rails in range(2, n):
        if n % rails != 0:
            continue
        chars_per_rail = n // rails
        result = []
        for i in range(chars_per_rail):
            for j in range(rails):
                idx = i + j * chars_per_rail
                if idx < n:
                    result.append(text[idx])
        results.append((rails, "".join(result)))
    return results


# ── Morse ───────────────────────────────────────────────────────────────────

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}

MORSE_REVERSE = {v: k for k, v in MORSE_CODE.items()}


def morse_encode(text):
    """文本 → 摩斯电码。"""
    words = text.upper().split()
    encoded_words = []
    for word in words:
        chars = [MORSE_CODE.get(c, c) for c in word if c.isalnum()]
        if chars:
            encoded_words.append(" ".join(chars))
    return "  ".join(encoded_words)


def morse_decode(morse):
    """摩斯电码 → 文本。"""
    words = morse.split("  ")
    decoded = []
    for word in words:
        chars = word.split()
        decoded.append("".join(MORSE_REVERSE.get(c, c) for c in chars))
    return " ".join(decoded)


# ── Bacon ───────────────────────────────────────────────────────────────────

BACON_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BACON_CODES_1 = [
    "aaaaa", "aaaab", "aaaba", "aaabb", "aabaa", "aabab", "aabba", "aabbb",
    "abaaa", "abaab", "ababa", "ababb", "abbaa", "abbab", "abbba", "abbbb",
    "baaaa", "baaab", "baaba", "baabb", "babaa", "babab", "babba", "babbb",
    "bbaaa", "bbaab",
]
BACON_CODES_2 = list(BACON_CODES_1)
# I/J and U/V share in the original Bacon cipher
BACON_CODES_2[8] = "abaaa"   # I = J
BACON_CODES_2[9] = "abaaa"   # J = I
BACON_CODES_2[20] = "baabb"  # U = V
BACON_CODES_2[21] = "baabb"  # V = U

BACON_MAP_1 = {c: k for c, k in zip(BACON_ALPHA, BACON_CODES_1)}
BACON_RMAP_1 = {k: c for c, k in BACON_MAP_1.items()}
BACON_MAP_2 = {c: k for c, k in zip(BACON_ALPHA, BACON_CODES_2)}
BACON_RMAP_2 = {k: c for c, k in BACON_MAP_2.items()}


def bacon_encode(text):
    """文本 → 培根密码 5 位编码。"""
    result = []
    for c in text.upper():
        if c in BACON_MAP_1:
            result.append(BACON_MAP_1[c])
    return "".join(result)


def bacon_decode(code):
    """5 位培根编码 → 文本（两种变体）。"""
    parts = re.findall(".{5}", code.replace(" ", ""))
    v1 = "".join(BACON_RMAP_1.get(p, "?") for p in parts)
    v2 = "".join(BACON_RMAP_2.get(p, "?") for p in parts)
    return v1, v2


# ── ADFGX / ADFGVX ─────────────────────────────────────────────────────────

def _get_adfgvx(use_v=False):
    try:
        if use_v:
            from pycipher import ADFGVX as Cipher
        else:
            from pycipher import ADFGX as Cipher
        return Cipher
    except ImportError:
        raise ImportError(
            "pycipher 未安装。运行: pip install pycipher"
        )


def _adfgvx_encrypt(text, key, use_v=False):
    Cipher = _get_adfgvx(use_v)
    if use_v:
        key_square = "ph0qg64mea1yl2nofdxkr3cvs5zw7bj9uti8"
    else:
        key_square = "phqgmeaynofdxkrcvszwbutil"
    c = Cipher(key_square, key)
    return c.encipher(text)


def _adfgvx_decrypt(text, key, use_v=False):
    Cipher = _get_adfgvx(use_v)
    if use_v:
        key_square = "ph0qg64mea1yl2nofdxkr3cvs5zw7bj9uti8"
    else:
        key_square = "phqgmeaynofdxkrcvszwbutil"
    c = Cipher(key_square, key)
    return c.decipher(text)


def adfgx_encrypt(text, key):
    return _adfgvx_encrypt(text, key, use_v=False)


def adfgx_decrypt(text, key):
    return _adfgvx_decrypt(text, key, use_v=False)


def adfgvx_encrypt(text, key):
    return _adfgvx_encrypt(text, key, use_v=True)


def adfgvx_decrypt(text, key):
    return _adfgvx_decrypt(text, key, use_v=True)


# ── XOR ─────────────────────────────────────────────────────────────────────

def xor_encrypt(text, key):
    """用密钥逐字节 XOR 加密，返回 hex。"""
    result = bytearray()
    kbytes = key.encode()
    for i, b in enumerate(text.encode()):
        result.append(b ^ kbytes[i % len(kbytes)])
    return result.hex()


def xor_decrypt(hex_str, key, encoding="utf-8"):
    """用密钥 XOR 解密 hex → 字符串。"""
    raw = bytes.fromhex(hex_str)
    result = bytearray()
    kbytes = key.encode()
    for i, b in enumerate(raw):
        result.append(b ^ kbytes[i % len(kbytes)])
    return result.decode(encoding, errors="replace")
