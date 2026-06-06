#!/usr/bin/env python3
"""哈希模块 — MD5, SHA1, SHA256, SHA512, NTLM 等。"""

import hashlib


def hash_md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def hash_sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()


def hash_sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()


def hash_sha512(s):
    return hashlib.sha512(s.encode()).hexdigest()


def hash_sha3_256(s):
    return hashlib.sha3_256(s.encode()).hexdigest()


def hash_sha3_512(s):
    return hashlib.sha3_512(s.encode()).hexdigest()


def hash_blake2b(s):
    return hashlib.blake2b(s.encode()).hexdigest()


def hash_blake2s(s):
    return hashlib.blake2s(s.encode()).hexdigest()


def hash_ntlm(s):
    """NTLM hash — 用于 Windows 认证测试。"""
    return hashlib.new("md4", s.encode("utf-16-le")).hexdigest()


ALL_HASHES = [
    ("MD5", hash_md5),
    ("MD5(16)", lambda s: hash_md5(s)[8:-8]),
    ("SHA1", hash_sha1),
    ("SHA256", hash_sha256),
    ("SHA512", hash_sha512),
    ("SHA3-256", hash_sha3_256),
    ("SHA3-512", hash_sha3_512),
    ("BLAKE2b", hash_blake2b),
    ("BLAKE2s", hash_blake2s),
    ("NTLM", hash_ntlm),
]


def compute_all(s):
    """计算所有支持的哈希并返回 (名称, 结果) 列表。"""
    return [(name, fn(s)) for name, fn in ALL_HASHES]
