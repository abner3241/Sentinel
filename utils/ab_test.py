def ab_test(symbols, strategy_name, param, val_a, val_b):
    """Roda comparação A/B de duas configurações de parâmetro para uma estratégia.
    Retorna dict com métricas de PnL e winrate para cada configuração.
    # TODO: implementar backtest histórico real
    return {
        "A": {"symbol": symbols, "strategy": strategy_name, param: val_a, "pnl": None, "winrate": None},
        "B": {"symbol": symbols, "strategy": strategy_name, param: val_b, "pnl": None, "winrate": None},

"""
# [AUTO-FIXED] }