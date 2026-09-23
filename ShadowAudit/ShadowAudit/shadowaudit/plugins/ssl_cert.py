"""Plugin que verifica o certificado SSL/TLS do alvo (validade, emissor, dias restantes)."""

import socket
import ssl
from datetime import datetime, timezone

from shadowaudit.plugins.base import AuditPlugin
from shadowaudit.utils.net import parse_target

TIMEOUT_SEGUNDOS = 5
DIAS_AVISO_EXPIRACAO = 30


def _campo_para_dict(campo_x509) -> dict:
    # certificado vem como tupla de tuplas, ex.: ((('commonName', 'exemplo.com'),),)
    resultado = {}
    for grupo in campo_x509:
        for chave, valor in grupo:
            resultado[chave] = valor
    return resultado


class SSLCertPlugin(AuditPlugin):

    name = "SSL/TLS Certificate"

    def run(self, target: str) -> dict:
        host, usa_https = parse_target(target)

        if not usa_https:
            return {
                "plugin": self.name,
                "target": target,
                "status": "ignorado",
                "motivo": "alvo usa http, nao ha certificado para verificar",
            }

        contexto = ssl.create_default_context()

        try:
            with socket.create_connection((host, 443), timeout=TIMEOUT_SEGUNDOS) as sock:
                with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    protocolo = ssock.version()
        except ConnectionRefusedError:
            return {
                "plugin": self.name,
                "target": target,
                "status": "ignorado",
                "motivo": "porta 443 fechada, o alvo nao parece servir HTTPS",
            }
        except (socket.timeout, socket.gaierror, ssl.SSLError) as exc:
            return {
                "plugin": self.name,
                "target": target,
                "status": "erro",
                "error": str(exc),
            }

        emissor = _campo_para_dict(cert.get("issuer", ()))
        titular = _campo_para_dict(cert.get("subject", ()))

        expira_em = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        dias_restantes = (expira_em - datetime.now(timezone.utc)).days

        return {
            "plugin": self.name,
            "target": target,
            "status": "executado",
            "protocolo_tls": protocolo,
            "emitido_para": titular.get("commonName", "desconhecido"),
            "emitido_por": emissor.get("commonName", "desconhecido"),
            "expira_em": expira_em.strftime("%Y-%m-%d"),
            "dias_restantes": dias_restantes,
            "expirado": dias_restantes < 0,
            "expira_em_breve": 0 <= dias_restantes <= DIAS_AVISO_EXPIRACAO,
        }
