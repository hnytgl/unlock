"""输出格式化与工具函数"""


def color(text, color_name="yellow"):
    """简易终端着色（兼容无 colorama 环境）。"""
    codes = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
        "bold": "\033[1m",
    }
    try:
        from colorama import init, Fore
        init(autoreset=True)
        color_map = {
            "red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW,
            "blue": Fore.BLUE, "magenta": Fore.MAGENTA, "cyan": Fore.CYAN,
        }
        return f"{color_map.get(color_name, Fore.YELLOW)}{text}{Fore.RESET}"
    except ImportError:
        c = codes.get(color_name, codes["yellow"])
        return f"{c}{text}{codes['reset']}"


def print_result(label, value, color_name="yellow"):
    """统一打印 标签 => 值 格式。"""
    print(f"  {color(label, 'cyan')} => {color(value, color_name)}")


def print_title(title):
    """打印标题分隔线。"""
    sep = "─" * 50
    print(f"\n{color(sep, 'blue')}")
    print(f"{color(title, 'magenta')}")
    print(f"{color(sep, 'blue')}")


def print_group(items, title="结果"):
    """打印一组结果。"""
    print_title(title)
    for label, val in items:
        print(f"  {color(label + ':', 'cyan'):20s} {color(val, 'yellow')}")
