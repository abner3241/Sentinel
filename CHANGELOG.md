# Changelog

- Versão inicial unificada.

## [31.0.0] - 2025-07-05
- Pacote versão 31.0.0 gerado com estrutura unificada.

## [32.0.0] - 2025-07-05
- Adicionado comando /run_backtest no Telegram.
- Criado utils/registro_lucros.py para métricas e daily PnL.
- Implementada enviar_alerta_telegram para envio direto.

## [32.0.0] - 2025-07-05
- Adicionado comando `/run_backtest` no Telegram.
- Módulo `utils/registro_lucros.py` para métricas implementado.
- Função `enviar_alerta_telegram` adicionada.

## [33.0.0] - 2025-07-05
- Adicionada interface de tuning no dashboard UI.
- Endpoints REST para `/api/retrain` e `/api/config`.
- Capacidade de ajustar thresholds dinamicamente via UI.

## [34.0.0] - 2025-07-05
- Comando `/saldo` implementado.
- Filtro de sinais no engine usando `RSI_THRESHOLD` e `PREDICTION_THRESHOLD`.
- Função `predict_latest` adicionada em strategies/ml.py.
- Agent de ajuste automático de thresholds em strategies/agent.py e agendado.

## [35.0.0] - 2025-07-05
- Agendamento de engine_loop em core/tasks.py
- Execução automática de ordens em strategies/engine.py usando ExchangeFactory e RiskManager
- Push automático de indicadores no technical_loop quando ativo (/indicadores_auto)
- Unificação das loops core e engine

## [36.0.0] - 2025-07-05
- Reintroduzidos módulos de v17:
  - services: arbitrage.py, contexto_externo.py, exportador_lucros.py, exportador_sinais.py, hedging.py, signals_chain.py
  - utils: analise_contexto.py, autoaprendizado.py, avg_buy.py, bracket.py, cache.py, circuit_breaker.py,
    coletor_contexto.py, explorador_falhas.py, exportador_csv.py, exportador_desempenho.py,
    notifications.py, performance_store.py, performance_tracker.py, persisty.py, predit0r.py,
    sparkline.py, storage.py, tradingview.py, train_model.py, train_spot_model.py
- Mantidas todas as funcionalidades existentes do bot (thresholds, ordens, indicadores, tuning UI, etc.).

## [37.0.0] - 2025-07-05
- Adicionados handlers especializados:
  - handlers/alerts.py
  - handlers/indicadores.py
  - handlers/performance.py
- Comandos de ordens:
  - /ordens, /cancelar
- Stub de gRPC gerado em grpc/sentinel_pb2.py e grpc/sentinel_pb2_grpc.py
- Adicionados Dockerfile e docker-compose.yml para deploy containerizado

## [38.0.0] - 2025-07-05
- Unified entrypoint in scripts/run.py executing FastAPI, tasks, Telegram, and gRPC in one loop with graceful shutdown.
- Added safe_handler decorator to handlers to catch errors and notify users.
- Implemented graceful shutdown of background tasks in core/tasks.py and core/app.py.
- Fixed Bybit V5 authentication in services/bybit_client.py with proper HMAC signature and header X-BAPI-SIGN-TYPE.
- Added Prometheus metrics (ORDER_COUNTER, ORDER_LATENCY, PNL_GAUGE) in utils/metrics.py and /metrics endpoint.
- Stubbed check_anomalies() in utils/reporter.py for future anomaly detection.
- Added GitHub Actions workflow (.github/workflows/release.yml) for semantic releases to PyPI.

- Adicionado comando /avg para mostrar avg buy de cada ativo.