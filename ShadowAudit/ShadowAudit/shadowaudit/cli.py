"""Interface de linha de comando do ShadowAudit."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shadowaudit",
        description="ShadowAudit - framework modular de auditoria de seguranca.",
    )

    parser.add_argument("--target", "-t", help="Alvo autorizado a ser auditado.")
    parser.add_argument("--config", "-c", default="config.yaml", help="Caminho do arquivo de configuracao.")
    parser.add_argument("--no-db", action="store_true", help="Nao salva os resultados no banco de dados.")
    parser.add_argument("--no-report", action="store_true", help="Nao gera relatorio JSON.")
    parser.add_argument("--no-banner", action="store_true", help="Nao exibe o banner no terminal.")
    parser.add_argument("--yes", "-y", action="store_true", help="Pula a confirmacao de autorizacao (uso em CI/scripts).")

    return parser


def parse_args(argv=None) -> argparse.Namespace:
    return build_parser().parse_args(argv)
