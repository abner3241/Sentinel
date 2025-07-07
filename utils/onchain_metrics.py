def get_onchain_flow(symbol: str, days: int = 7):
    """Retorna fluxo on-chain de exchanges nos últimos `days` dias para o símbolo."""
    # TODO: integrar API Glassnode ou similar para dados reais
    return {
        "symbol": symbol,
        "days": days,
        "exchange_inflow": None,
        "exchange_outflow": None,
        "net_flow": None
}