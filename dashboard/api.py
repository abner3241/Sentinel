import prometheus_client
from fastapi import APIRouter
from utils.reporter import Reporter

router = APIRouter()

import asyncio
from utils.config_manager import ConfigManager
from strategies.ml import run_ml_pipeline


@router.post("/retrain")
async def retrain_model():
    """Inicia re-treinamento do modelo em segundo plano"""
    asyncio.create_task(run_ml_pipeline())
    return {"status": "Model retraining started"}

@router.get("/config")
async def get_config():
    """Retorna todas as configurações atuais"""
    return ConfigManager.list_all()

@router.get("/config/{key}")
async def get_config_key(key: str):
    """Retorna valor de uma configuração específica"""
    value = ConfigManager.get(key)
    return {key: value}

@router.post("/config")
async def set_config(key: str, value: str):
    """Define valores de configuração em tempo de execução"""
    ConfigManager.set(key, value)
    return {"status": "Config updated", "key": key, "value": value}


@router.get("/status")
async def get_status():
    reporter = Reporter()
    return {"status": reporter.get_status()}

@router.get("/signals")
async def get_signals():
    reporter = Reporter()
    return {"signals": reporter._load_json(reporter.signals_file)}

@router.get("/logs")
async def get_logs(limit: int = 50):
    reporter = Reporter()
    return {"logs": reporter.get_recent_logs(limit)}

@router.get("/performance")
async def get_performance():
    reporter = Reporter()
    return {"performance": reporter.get_performance_report()}

from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from utils.metrics import registry

@router.get("/metrics")
async def get_metrics():
    data = generate_latest(registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
