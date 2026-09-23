# ShadowAudit

Framework modular de auditoria de segurança desenvolvido em Python.

## Sobre

ShadowAudit é um framework baseado em plugins para auditoria de segurança em ambientes **autorizados**. A ideia central é permitir que cada verificação (scanner, checagem de configuração, coleta de evidência etc.) seja implementada como um plugin independente, orquestrado por um runner central.

## Arquitetura

```
ShadowAudit/
├── shadowaudit/
│   ├── core/          # Runner, logger, config
│   ├── plugins/        # Plugins de auditoria (base + implementações)
│   ├── scanners/        # Scanners (a implementar)
│   ├── reports/          # Geração de relatórios (JSON)
│   ├── database/          # Persistência em SQLite
│   └── utils/               # Utilitários gerais
├── tests/                # Testes automatizados (pytest)
├── config.yaml           # Configuração do projeto
└── requirements.txt
```

## Instalação

```bash
git clone https://github.com/K4KU404/ShadowAudit.git
cd ShadowAudit

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Uso

```bash
python -m shadowaudit.main --target laboratorio.local
```

Ou de forma interativa, sem o parâmetro `--target`:

```bash
python -m shadowaudit.main
```

Ao final da execução, os resultados são:
- salvos no banco SQLite (`database/shadowaudit.db`)
- exportados como relatório JSON em `reports_output/`

Para pular alguma dessas etapas:

```bash
python -m shadowaudit.main --target laboratorio.local --no-db --no-report
```

## Testes

```bash
pytest -v
```

## Criando um novo plugin

Todo plugin herda de `AuditPlugin` e implementa o método `run`:

```python
from shadowaudit.plugins.base import AuditPlugin


class MeuPlugin(AuditPlugin):
    name = "Meu Plugin"

    def run(self, target: str) -> dict:
        # lógica de auditoria aqui
        return {"plugin": self.name, "target": target, "status": "executado"}
```

Depois, registre o plugin em `AVAILABLE_PLUGINS` (`shadowaudit/main.py`) e adicione o nome em `config.yaml`, na seção `plugins.enabled`.

## Roadmap

- [x] Estrutura do projeto
- [x] Runner
- [x] Sistema de plugins
- [x] Plugin de exemplo
- [x] Logger
- [x] CLI
- [x] Configuração (YAML)
- [x] Persistência em SQLite
- [x] Relatório JSON
- [x] Testes automatizados
- [x] GitHub Actions (CI)
- [ ] Scanner modular real
- [ ] Sistema de evidências
- [ ] Dashboard

## Licença

MIT
