"""Plugin que verifica a presenca de cabecalhos HTTP de seguranca no alvo."""

import requests

from shadowaudit.plugins.base import AuditPlugin
from shadowaudit.utils.net import parse_target

# Cabecalhos de seguranca que esperamos encontrar numa resposta HTTP
CABECALHOS_SEGURANCA = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
]


class HTTPHeadersPlugin(AuditPlugin):

    name = "HTTP Security Headers"

    def run(self, target: str) -> dict:
        host, usa_https = parse_target(target)
        esquemas = ["https", "http"] if usa_https else ["http", "https"]

        response = None
        ultimo_erro = None

        for esquema in esquemas:
            try:
                response = requests.get(f"{esquema}://{host}", timeout=10)
                break
            except requests.RequestException as exc:
                ultimo_erro = exc

        if response is None:
            return {
                "plugin": self.name,
                "target": target,
                "status": "erro",
                "error": str(ultimo_erro),
            }

        presentes = [h for h in CABECALHOS_SEGURANCA if h in response.headers]
        ausentes = [h for h in CABECALHOS_SEGURANCA if h not in response.headers]

        return {
            "plugin": self.name,
            "target": target,
            "status": "executado",
            "url_usada": response.url,
            "status_code": response.status_code,
            "headers_presentes": presentes,
            "headers_ausentes": ausentes,
        }
