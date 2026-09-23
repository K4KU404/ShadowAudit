"""Plugin que verifica quais portas TCP comuns estao abertas no alvo.

Faz apenas uma tentativa de conexao TCP (connect scan) em cada porta,
sem enviar payload nenhum. E o equivalente a um "nmap -sT" simples.
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from shadowaudit.plugins.base import AuditPlugin
from shadowaudit.utils.net import parse_target

# Portas comuns verificadas por padrao. Pode ser sobrescrito via config.yaml.
PORTAS_PADRAO = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080, 8443]

TIMEOUT_SEGUNDOS = 1.5


def _checar_porta(host: str, porta: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT_SEGUNDOS)
        return sock.connect_ex((host, porta)) == 0


def _nome_servico(porta: int) -> str:
    try:
        return socket.getservbyport(porta)
    except OSError:
        return "desconhecido"


class PortScannerPlugin(AuditPlugin):

    name = "Port Scanner"

    def __init__(self, portas=None):
        self.portas = portas or PORTAS_PADRAO

    def run(self, target: str) -> dict:
        host, _ = parse_target(target)

        try:
            socket.gethostbyname(host)
        except socket.gaierror as exc:
            return {
                "plugin": self.name,
                "target": target,
                "status": "erro",
                "error": f"Nao foi possivel resolver o host: {exc}",
            }

        abertas = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            futuros = {executor.submit(_checar_porta, host, p): p for p in self.portas}
            for futuro in as_completed(futuros):
                porta = futuros[futuro]
                if futuro.result():
                    abertas.append(porta)

        abertas.sort()

        return {
            "plugin": self.name,
            "target": target,
            "host": host,
            "status": "executado",
            "portas_verificadas": len(self.portas),
            "portas_abertas": [{"porta": p, "servico": _nome_servico(p)} for p in abertas],
        }
