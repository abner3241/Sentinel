# Sentinel

**Sentinel** é um bot de trading automatizado para criptomoedas, combinando análise técnica, inteligência artificial, alertas em tempo real via Telegram, execução por API e um painel de controle via FastAPI. Projetado para ser modular, extensível e seguro, o Sentinel é uma plataforma de pesquisa e operação real para estratégias de mercado.

> 📜 Este projeto é open-source para fins educacionais e colaborativos.  
> ❌ Uso comercial e redistribuição não são permitidos sem autorização.  
> Veja o arquivo [LICENSE.md](./LICENSE.md) para detalhes.

## ✨ Funcionalidades principais

- Estratégias com RSI, Bollinger, ATR, multi-take-profit e IA
- Execução real (Bybit) ou simulada (DryRun)
- Predição baseada em IA e sentimento de mercado (NewsAPI + VADER)
- Envio de sinais, alertas e comandos via Telegram
- Dashboard FastAPI com rotas `/status`, `/signals`, `/logs`, `/performance`, `/config`, `/metrics`
- Integração com Prometheus para métricas e Grafana para visualização
- CLI com `run`, `backtest`, `gen-grpc`, `train` e muito mais
- Suporte a gRPC + scripts `generate_grpc.sh`

## 📦 Arquitetura

Sentinel/
├── core/                  # Inicialização (FastAPI, loops, CLI)
├── handlers/              # Comandos do bot Telegram
├── strategies/            # Técnicas + IA + filtragem de sinais
├── utils/                 # Ferramentas auxiliares e técnicas
├── services/              # Conectores de API (Bybit, Binance, NewsAPI)
├── dashboard/             # API e UI via FastAPI
├── grpc/                  # Stubs gerados do proto
├── proto/                 # Arquivos .proto de definição gRPC
├── scripts/               # Scripts auxiliares de execução e análise
├── sinais.json            # Sinais ativos (não versionado)
├── historico_sinais.json  # Histórico (não versionado)

## ⚙️ Requisitos

- Python 3.12+
- pip, virtualenv (ou poetry)
- Docker (opcional para ambiente isolado)

## 🚀 Executando

```bash
# Ative seu ambiente e instale dependências
pip install -r requirements.txt

# Execute o projeto (modo local)
python run.py

🛡 Licença

Ver arquivo LICENSE.md

Este projeto é open-source, mas com uso restrito não comercial.
Para uso comercial, integração com plataformas ou licenciamento, contate:
📧 abnervicente65@gmail.com
