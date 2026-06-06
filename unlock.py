#!/usr/bin/env python3
"""
unlock — 终端编码解码与加解密工具箱

支持 URL、Base64、HTML、Hex、Unicode、进制转换、哈希、
凯撒、维吉尼亚、培根、ADFGX/ADFGVX、摩斯、Atbash 等。

用法:
  python unlock.py -h          # 查看所有命令
  python unlock.py url 数据    # URL 编码
  python unlock.py md5 数据    # MD5 哈希
"""

import argparse
import sys
import textwrap

from unlock_cli import __version__
from unlock_cli.crypto import (
    adfgx_decrypt, adfgx_encrypt, adfgvx_decrypt, adfgvx_encrypt,
    atbash, bacon_decode, bacon_encode, caesar_bruteforce,
    caesar_decrypt, caesar_encrypt, morse_decode, morse_encode,
    rail_fence_decrypt, rot13, rot47, vigenere_decrypt, vigenere_encrypt,
    xor_decrypt, xor_encrypt,
)
from unlock_cli.encoders import (
    b64_decode, b64_encode, b64_urlsafe_decode, b64_urlsafe_encode,
    chinese_to_hex_gbk, chinese_to_hex_utf8, from_binary, from_decimal,
    from_octal, hex_to_chinese, hex_to_str, html_decode, html_encode,
    int_to_ip, ip_to_int, str_info, str_reverse, str_to_hex,
    to_binary, to_decimal, to_octal, unicode_decode, unicode_encode,
    url_decode, url_encode, url_encode_component,
)
from unlock_cli.hashes import compute_all, hash_md5, hash_ntlm, hash_sha256
from unlock_cli.utils import color, print_group, print_result, print_title


def build_parser():
    parser = argparse.ArgumentParser(
        description=f"unlock v{__version__} — 终端编码解码与加解密工具箱",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            示例:
              python unlock.py url "你好世界"
              python unlock.py b64 "SGVsbG8="
              python unlock.py md5 "hello"
              python unlock.py all "hello"
              python unlock.py caesar "KroDv" 3
              python unlock.py morse ".... . .-.. .-.. ---"
              python unlock.py xor "hello" "key"
              python unlock.py info "hello world"
              python unlock.py interact
        """),
    )

    parser.add_argument(
        "command", nargs="?",
        help="操作命令（不带参数进入交互模式）",
    )
    parser.add_argument(
        "args", nargs="*",
        help="操作参数（依赖于具体命令）",
    )
    parser.add_argument(
        "-v", "--version", action="store_true",
        help="显示版本号",
    )
    return parser


def show_help():
    banner = r"""
     _            _
  _ | | ___   ___| | __
 | | | |/ _ \ / __| |/ /
 | |_| | (_) | (__|   <
  \__,_|\___/ \___|_|\_\    v%s
""" % __version__

    print(color(banner, "magenta"))
    print(color("═" * 55, "cyan"))
    print(color("  编码/解码", "green"))
    print(color("═" * 55, "cyan"))
    cmds = [
        ("url  <text>", "URL 编码"),
        ("urld <text>", "URL 解码"),
        ("b64  <text>", "Base64 编码"),
        ("b64d <text>", "Base64 解码"),
        ("b64u <text>", "URL-safe Base64 编码"),
        ("b64ud <text>", "URL-safe Base64 解码"),
        ("hex  <text>", "字符串 → 十六进制"),
        ("hexd <hex>", "十六进制 → 字符串"),
        ("html <text>", "HTML 实体编码"),
        ("htmld <text>", "HTML 实体解码"),
        ("uni  <text>", "中文 → Unicode 转义"),
        ("unid <text>", "Unicode 转义 → 中文"),
        ("hexc <text>", "中文 → 十六进制 (UTF-8 + GBK)"),
        ("bin  <text>", "字符串 → 二进制"),
        ("oct  <text>", "字符串 → 八进制"),
        ("dec  <text>", "字符串 → 十进制"),
        ("bind <bin>", "二进制 → 字符串"),
        ("octd <oct>", "八进制 → 字符串"),
        ("decd <dec>", "十进制 → 字符串"),
        ("rev  <text>", "字符串反转"),
        ("info <text>", "字符串统计信息"),
        ("ip2i <ip>",  "IP 地址 → 整数"),
        ("i2ip <num>", "整数 → IP 地址"),
    ]
    for cmd, desc in cmds:
        print(f"  {color(cmd.ljust(20), 'yellow')} {desc}")

    print()
    print(color("═" * 55, "cyan"))
    print(color("  哈希", "green"))
    print(color("═" * 55, "cyan"))
    for cmd, desc in [
        ("md5  <text>", "MD5 哈希"),
        ("sha256 <text>", "SHA-256 哈希"),
        ("ntlm <text>", "NTLM 哈希"),
        ("all  <text>", "所有哈希"),
    ]:
        print(f"  {color(cmd.ljust(20), 'yellow')} {desc}")

    print()
    print(color("═" * 55, "cyan"))
    print(color("  加/解密", "green"))
    print(color("═" * 55, "cyan"))
    cmds = [
        ("caesar <text> <n>", "凯撒加密 (偏移 n)"),
        ("caesard <text> <n>", "凯撒解密"),
        ("caesarx <text>", "凯撒暴力破解 (1-25)"),
        ("rot13 <text>", "ROT13"),
        ("rot47 <text>", "ROT47"),
        ("atbash <text>", "Atbash 密码"),
        ("vig <text> <key>", "维吉尼亚加密"),
        ("vigd <text> <key>", "维吉尼亚解密"),
        ("morse <text>", "摩斯电码编码"),
        ("morsed <text>", "摩斯电码解码"),
        ("bacon <text>", "培根密码编码"),
        ("bacond <code>", "培根密码解码"),
        ("fence <text>", "栅栏密码解密"),
        ("adfgx <text> <key>", "ADFGX 加密"),
        ("adfgxd <text> <key>", "ADFGX 解密"),
        ("adfgvx <text> <key>", "ADFGVX 加密"),
        ("adfgvxd <text> <key>", "ADFGVX 解密"),
        ("xor <text> <key>", "XOR 加密 (返回 hex)"),
        ("xord <hex> <key>", "XOR 解密"),
    ]
    for cmd, desc in cmds:
        print(f"  {color(cmd, 'yellow'):23s} {desc}")

    print()
    print(color("═" * 55, "cyan"))
    print(color("  交互/其他", "green"))
    print(color("═" * 55, "cyan"))
    print(f"  {color('interact', 'yellow'):23s} 交互模式")
    print(f"  {color('--version', 'yellow'):23s} 显示版本")
    print(f"  {color('--help', 'yellow'):23s} 显示此帮助")
    print(color("═" * 55, "cyan"))
    print()


CMD_MAP = {}


def register(cmd_names):
    """Decorator to register a command handler."""
    def wrapper(fn):
        if isinstance(cmd_names, str):
            names = [cmd_names]
        else:
            names = cmd_names
        for n in names:
            CMD_MAP[n] = fn
        return fn
    return wrapper


# ── Encoders ────────────────────────────────────────────────────────────────

@register(["url"])
def cmd_url(args):
    print_result("URL 编码", url_encode(args[0]))


@register(["urld"])
def cmd_urld(args):
    print_result("URL 解码", url_decode(args[0]))


@register(["b64"])
def cmd_b64(args):
    print_result("Base64 编码", b64_encode(args[0]))


@register(["b64d"])
def cmd_b64d(args):
    print_result("Base64 解码", b64_decode(args[0]))


@register(["b64u"])
def cmd_b64u(args):
    print_result("URL Safe Base64", b64_urlsafe_encode(args[0]))


@register(["b64ud"])
def cmd_b64ud(args):
    print_result("URL Safe Base64 解码", b64_urlsafe_decode(args[0]))


@register(["hex"])
def cmd_hex(args):
    print_result("字符串→十六进制 (UTF-8)", str_to_hex(args[0]))


@register(["hexd"])
def cmd_hexd(args):
    print_result("十六进制→字符串", hex_to_str(args[0]))


@register(["html"])
def cmd_html(args):
    print_result("HTML 编码", html_encode(args[0]))


@register(["htmld"])
def cmd_htmld(args):
    print_result("HTML 解码", html_decode(args[0]))


@register(["uni"])
def cmd_uni(args):
    print_result("中文→Unicode", unicode_encode(args[0]))


@register(["unid"])
def cmd_unid(args):
    print_result("Unicode→中文", unicode_decode(args[0]))


@register(["hexc"])
def cmd_hexc(args):
    print_group([
        ("Hex (UTF-8)", chinese_to_hex_utf8(args[0])),
        ("Hex (GBK)", chinese_to_hex_gbk(args[0])),
    ], "中文 → 十六进制")


@register(["bin"])
def cmd_bin(args):
    print_result("二进制", to_binary(args[0]))


@register(["oct"])
def cmd_oct(args):
    print_result("八进制", to_octal(args[0]))


@register(["dec"])
def cmd_dec(args):
    print_result("十进制", to_decimal(args[0]))


@register(["bind"])
def cmd_bind(args):
    print_result("二进制→字符串", from_binary(args[0]))


@register(["octd"])
def cmd_octd(args):
    print_result("八进制→字符串", from_octal(args[0]))


@register(["decd"])
def cmd_decd(args):
    print_result("十进制→字符串", from_decimal(args[0]))


@register(["rev"])
def cmd_rev(args):
    print_result("反转", str_reverse(args[0]))


@register(["info"])
def cmd_info(args):
    s = args[0]
    info = str_info(s)
    print_group(list(info.items()), f"字符串信息: '{s[:30]}'")


@register(["ip2i"])
def cmd_ip2i(args):
    print_result("IP → 整数", str(ip_to_int(args[0])))


@register(["i2ip"])
def cmd_i2ip(args):
    print_result("整数 → IP", int_to_ip(int(args[0])))


# ── Hashes ──────────────────────────────────────────────────────────────────

@register(["md5"])
def cmd_md5(args):
    r = hash_md5(args[0])
    print_group([
        ("MD5 (32)", r),
        ("MD5 (16)", r[8:-8]),
    ], f"MD5: '{args[0]}'")


@register(["sha256"])
def cmd_sha256(args):
    print_result("SHA-256", hash_sha256(args[0]))


@register(["ntlm"])
def cmd_ntlm(args):
    print_result("NTLM Hash", hash_ntlm(args[0]))


@register(["all"])
def cmd_all(args):
    results = compute_all(args[0])
    print_group(results, "全部哈希")


# ── Crypto ──────────────────────────────────────────────────────────────────

@register(["caesar"])
def cmd_caesar(args):
    n = int(args[1]) if len(args) > 1 else 3
    print_result(f"凯撒加密 (偏移 {n})", caesar_encrypt(args[0], n))


@register(["caesard"])
def cmd_caesard(args):
    n = int(args[1]) if len(args) > 1 else 3
    print_result(f"凯撒解密 (偏移 {n})", caesar_decrypt(args[0], n))


@register(["caesarx"])
def cmd_caesarx(args):
    results = caesar_bruteforce(args[0])
    print_title(f"凯撒暴力破解: '{args[0]}'")
    for shift, text in results.items():
        print(f"  {color(f'偏移 {shift:2d}:', 'cyan'):12s} {text}")


@register(["rot13"])
def cmd_rot13(args):
    print_result("ROT13", rot13(args[0]))


@register(["rot47"])
def cmd_rot47(args):
    print_result("ROT47", rot47(args[0]))


@register(["atbash"])
def cmd_atbash(args):
    print_result("Atbash", atbash(args[0]))


@register(["vig"])
def cmd_vig(args):
    if len(args) < 2:
        print(color("[!] 用法: vig <明文> <密钥>", "red"))
        return
    print_result("维吉尼亚加密", vigenere_encrypt(args[0], args[1]))


@register(["vigd"])
def cmd_vigd(args):
    if len(args) < 2:
        print(color("[!] 用法: vigd <密文> <密钥>", "red"))
        return
    print_result("维吉尼亚解密", vigenere_decrypt(args[0], args[1]))


@register(["morse"])
def cmd_morse(args):
    print_result("摩斯电码", morse_encode(args[0]))


@register(["morsed"])
def cmd_morsed(args):
    print_result("摩斯解码", morse_decode(args[0]))


@register(["bacon"])
def cmd_bacon(args):
    print_result("培根编码", bacon_encode(args[0]))


@register(["bacond"])
def cmd_bacond(args):
    v1, v2 = bacon_decode(args[0])
    print_group([("变体 1 (I=J, U=V)", v1), ("变体 2", v2)], "培根解码")


@register(["fence"])
def cmd_fence(args):
    results = rail_fence_decrypt(args[0])
    print_title(f"栅栏密码: '{args[0]}'")
    for rails, text in results:
        print(f"  {color(f'栏数 {rails:2d}:', 'cyan'):12s} {text}")


@register(["adfgx", "adfgxd", "adfgvx", "adfgvxd"])
def cmd_adfgx(args):
    cmd = sys.argv[1].lower()
    if len(args) < 2:
        print(color(f"[!] 用法: {sys.argv[1]} <文本> <密钥>", "red"))
        return
    try:
        if cmd == "adfgx":
            print_result("ADFGX 加密", adfgx_encrypt(args[0], args[1]))
        elif cmd == "adfgxd":
            print_result("ADFGX 解密", adfgx_decrypt(args[0], args[1]))
        elif cmd == "adfgvx":
            print_result("ADFGVX 加密", adfgvx_encrypt(args[0], args[1]))
        elif cmd == "adfgvxd":
            print_result("ADFGVX 解密", adfgvx_decrypt(args[0], args[1]))
    except ImportError as e:
        print(color(f"[!] {e}", "red"))
    except Exception as e:
        print(color(f"[!] 错误: {e}", "red"))


@register(["xor"])
def cmd_xor(args):
    if len(args) < 2:
        print(color("[!] 用法: xor <文本> <密钥>", "red"))
        return
    print_result("XOR 加密 (hex)", xor_encrypt(args[0], args[1]))


@register(["xord"])
def cmd_xord(args):
    if len(args) < 2:
        print(color("[!] 用法: xord <hex> <密钥>", "red"))
        return
    print_result("XOR 解密", xor_decrypt(args[0], args[1]))


# ── Interactive Mode ────────────────────────────────────────────────────────

def interactive_mode():
    print(color("\n🧠 unlock 交互模式 (输入 'help' 查看命令, 'exit' 退出)\n", "green"))
    while True:
        try:
            line = input(color("unlock> ", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line.lower() in ("exit", "quit", "q"):
            break
        if line.lower() in ("help", "?"):
            show_help()
            continue

        parts = line.split()
        cmd = parts[0].lower()
        rest = parts[1:]
        handler = CMD_MAP.get(cmd)
        if handler:
            try:
                handler(rest)
            except Exception as e:
                print(color(f"[!] 错误: {e}", "red"))
        else:
            print(color(f"[!] 未知命令: {cmd} (输入 help 查看所有命令)", "red"))


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args, unknown = parser.parse_known_args()

    if args.version:
        print(f"unlock v{__version__}")
        return

    if not args.command or args.command == "help":
        show_help()
        return

    if args.command == "interact":
        interactive_mode()
        return

    handler = CMD_MAP.get(args.command.lower())
    if not handler:
        print(color(f"[!] 未知命令: {args.command}", "red"))
        print(color("    输入 python unlock.py -h 查看所有命令", "yellow"))
        sys.exit(1)

    cmd_args = args.args + unknown
    if not cmd_args:
        print(color(f"[!] 缺少参数: {args.command}", "red"))
        print(color("    输入 python unlock.py -h 查看用法", "yellow"))
        sys.exit(1)

    try:
        handler(cmd_args)
    except Exception as e:
        print(color(f"[!] 错误: {e}", "red"))
        sys.exit(1)


if __name__ == "__main__":
    main()
