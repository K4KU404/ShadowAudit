"""Banner exibido no terminal ao iniciar o ShadowAudit."""

from colorama import Fore, Style, init

init(autoreset=True)

VERSION = "0.1.0"

BANNER = r"""
   _____ __             __               ___             ___ __
  / ___// /_  ____ _____/ /___ _      __ /   |  __  ______/ (_) /_
  \__ \/ __ \/ __ `/ __  / __ \ | /| / // /| | / / / / __  / / __/
 ___/ / / / / /_/ / /_/ / /_/ / |/ |/ // ___ |/ /_/ / /_/ / / /_
/____/_/ /_/\__,_/\__,_/\____/|__/|__//_/  |_|\__,_/\__,_/_/\__/
"""


def print_banner():
    print(Fore.CYAN + BANNER)
    print(Fore.WHITE + f"  Framework de auditoria de seguranca  ·  v{VERSION}")
    print(Style.DIM + "  Use apenas em alvos que voce tem autorizacao para testar.\n")
