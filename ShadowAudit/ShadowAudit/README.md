# ShadowAudit

Framework modular de auditoria de seguranca desenvolvido em Python.

```
   _____ __             __               ___             ___ __
  / ___// /_  ____ _____/ /___ _      __ /   |  __  ______/ (_) /_
  \__ \/ __ \/ __ `/ __  / __ \ | /| / // /| | / / / / __  / / __/
 ___/ / / / / /_/ / /_/ / /_/ / |/ |/ // ___ |/ /_/ / /_/ / / /_
/____/_/ /_/\__,_/\__,_/\____/|__/|__//_/  |_|\__,_/\__,_/_/\__/
```

## Sobre

ShadowAudit e um framework baseado em plugins para auditoria de seguranca em ambientes **autorizados**. Cada verificacao (scanner, checagem de cabecalhos, coleta de evidencia etc.) e implementada como um plugin independente, orquestrado por um runner central.

> Use apenas contra alvos que voce tem autorizacao explicita para testar.

## Arquitetura

```
ShadowAudit/
├── shadowaudit/
│   ├── core/          # runner, logger, config, banner
│   ├── plugins/        # plugins de auditoria (base + implementacoes)
│   ├── scanners/         # scanners (a implementar)
│   ├── reports/            # geracao de relatorios (JSON)
│   ├── database/             # persistencia em SQLite
│   └── utils/                  # utilitarios gerais
├── tests/                # testes automatizados (pytest)
├── config.yaml           # configuracao do projeto
└── requirements.txt
```

## Instalacao

```bash
git clone https://github.com/K4KU404/ShadowAudit.git
cd ShadowAudit

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

## Uso

```bash
python -m shadowaudit.main --target https://exemplo.com
```

Ou de forma interativa, sem `--target`:

```bash
python -m shadowaudit.main
```

Flags disponiveis:

| Flag | Descricao |
|---|---|
| `--target`, `-t` | Alvo a ser auditado |
| `--config`, `-c` | Caminho do arquivo de configuracao (padrao: `config.yaml`) |
| `--no-db` | Nao salva os resultados no banco de dados |
| `--no-report` | Nao gera relatorio JSON |
| `--no-banner` | Nao exibe o banner no terminal |
| `--yes`, `-y` | Pula a confirmacao de autorizacao (uso em CI/scripts) |

Antes de executar, o ShadowAudit pede uma confirmacao de que voce tem autorizacao para auditar o alvo informado (pode ser pulada com `--yes`). Ao final, os resultados sao salvos em `database/shadowaudit.db` e exportados como JSON em `reports_output/`.

## Plugins disponiveis

- **HTTPHeadersPlugin** — checa a presenca de cabecalhos HTTP de seguranca (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`) na resposta do alvo.
- **SSLCertPlugin** — verifica o certificado TLS do alvo: emissor, protocolo, data de expiracao e quantos dias faltam para vencer.
- **PortScannerPlugin** — connect scan (`nmap -sT` simplificado) contra um conjunto de portas TCP comuns (21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080, 8443), sem enviar nenhum payload alem do handshake TCP.
- **ExamplePlugin** — plugin de referencia, nao faz verificacao real. Desabilitado por padrao em `config.yaml`.

## Testes

```bash
pytest -v
```

## Criando um novo plugin

```python
from shadowaudit.plugins.base import AuditPlugin


class MeuPlugin(AuditPlugin):
    name = "Meu Plugin"

    def run(self, target: str) -> dict:
        # logica de auditoria aqui
        return {"plugin": self.name, "target": target, "status": "executado"}
```

Depois, registre em `AVAILABLE_PLUGINS` (`shadowaudit/main.py`) e adicione o nome em `config.yaml`, na secao `plugins.enabled`.

## Roadmap

- [x] Estrutura do projeto
- [x] Runner
- [x] Sistema de plugins
- [x] Logger
- [x] CLI
- [x] Configuracao (YAML)
- [x] Banner no terminal
- [x] SQLite + relatorio JSON
- [x] Testes automatizados
- [x] GitHub Actions (CI)
- [x] Plugin: cabecalhos HTTP de seguranca
- [x] Plugin: certificado SSL/TLS
- [x] Plugin: scanner de portas
- [x] Confirmacao de autorizacao antes de auditar
- [ ] Sistema de evidencias
- [ ] Dashboard

## Licenca

MIT
