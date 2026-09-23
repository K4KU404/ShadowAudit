"""Funcoes auxiliares para interpretar o alvo informado pelo usuario."""

from urllib.parse import urlparse


def parse_target(target: str) -> tuple[str, bool]:
    """
    Recebe o alvo (URL ou hostname puro) e retorna (host, usa_https).

    Exemplos:
        "https://exemplo.com"  -> ("exemplo.com", True)
        "http://exemplo.com"   -> ("exemplo.com", False)
        "exemplo.com"          -> ("exemplo.com", True)
    """
    if "://" not in target:
        target = f"https://{target}"

    parsed = urlparse(target)
    host = parsed.hostname or target
    usa_https = parsed.scheme != "http"

    return host, usa_https
