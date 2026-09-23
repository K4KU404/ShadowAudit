"""Formata e imprime os resultados da auditoria de forma organizada no terminal."""

import os

from colorama import Fore, Style

LINHA = "─" * 60


def clear_screen():
    """Limpa o terminal (funciona no Windows, Linux e Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def _titulo(texto: str, cor=Fore.WHITE):
    print(f"\n{cor}{Style.BRIGHT}{texto}{Style.RESET_ALL}")
    print(Fore.BLACK + Style.BRIGHT + LINHA)


def _campo(rotulo: str, valor):
    print(f"  {Fore.WHITE}{rotulo:<20}{Style.RESET_ALL}{valor}")


def _print_http_headers(r: dict):
    _titulo(f"🔎 {r['plugin']}", Fore.CYAN)

    if r["status"] != "executado":
        print(f"  {Fore.YELLOW}{r.get('error') or r.get('motivo', 'nao executado')}")
        return

    _campo("URL", r["url_usada"])
    _campo("Status HTTP", r["status_code"])

    if r["headers_presentes"]:
        print(f"  {Fore.GREEN}Presentes:")
        for h in r["headers_presentes"]:
            print(f"    {Fore.GREEN}✓ {h}")

    if r["headers_ausentes"]:
        print(f"  {Fore.RED}Ausentes:")
        for h in r["headers_ausentes"]:
            print(f"    {Fore.RED}✗ {h}")


def _print_ssl_cert(r: dict):
    _titulo(f"🔐 {r['plugin']}", Fore.CYAN)

    if r["status"] == "ignorado":
        print(f"  {Fore.YELLOW}{r['motivo']}")
        return
    if r["status"] != "executado":
        print(f"  {Fore.RED}{r.get('error', 'erro desconhecido')}")
        return

    _campo("Protocolo", r["protocolo_tls"])
    _campo("Emitido para", r["emitido_para"])
    _campo("Emitido por", r["emitido_por"])

    if r["expirado"]:
        cor_validade, status_validade = Fore.RED, f"expirado ha {-r['dias_restantes']} dia(s)"
    elif r["expira_em_breve"]:
        cor_validade, status_validade = Fore.YELLOW, f"expira em {r['dias_restantes']} dia(s)"
    else:
        cor_validade, status_validade = Fore.GREEN, f"valido por {r['dias_restantes']} dia(s)"

    _campo("Validade", f"{cor_validade}{r['expira_em']} ({status_validade}){Style.RESET_ALL}")


def _print_port_scanner(r: dict):
    _titulo(f"🛰️  {r['plugin']}", Fore.CYAN)

    if r["status"] != "executado":
        print(f"  {Fore.RED}{r.get('error', 'erro desconhecido')}")
        return

    _campo("Host", r["host"])
    _campo("Portas verificadas", r["portas_verificadas"])

    if not r["portas_abertas"]:
        print(f"  {Fore.GREEN}Nenhuma porta aberta encontrada.")
        return

    print(f"  {Fore.YELLOW}Portas abertas:")
    for p in r["portas_abertas"]:
        print(f"    {Fore.YELLOW}● {p['porta']:<6}{Style.RESET_ALL}{p['servico']}")


def _print_generico(r: dict):
    _titulo(f"🧩 {r.get('plugin', 'Plugin')}", Fore.CYAN)
    for chave, valor in r.items():
        if chave in ("plugin", "target"):
            continue
        _campo(chave, valor)


_FORMATADORES = {
    "HTTP Security Headers": _print_http_headers,
    "SSL/TLS Certificate": _print_ssl_cert,
    "Port Scanner": _print_port_scanner,
}


def print_results(target: str, results: list):
    """Imprime todos os resultados da auditoria de forma organizada."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}AUDITORIA: {target}{Style.RESET_ALL}")

    for r in results:
        formatador = _FORMATADORES.get(r.get("plugin"), _print_generico)
        formatador(r)

    total = len(results)
    erros = sum(1 for r in results if r.get("status") == "erro")
    ok = total - erros

    print(f"\n{Fore.BLACK}{Style.BRIGHT}{LINHA}")
    resumo_cor = Fore.GREEN if erros == 0 else Fore.YELLOW
    print(f"{resumo_cor}{ok}/{total} plugin(s) concluido(s) sem erro.{Style.RESET_ALL}\n")
