import numpy as np

def run_monte_carlo(initial_balance: float,
                    num_simulations: int = 1000,
                    days: int = 30,
                    mean_return: float = 0.01,
                    volatility: float = 0.02):
    """Executa simulação Monte Carlo de PnL:
    - Gera trajetórias de retorno diário baseado em distribuição normal.
    - Retorna estatísticas agregadas.
    # Simulate daily returns: shape (num_simulations, days)
    returns = np.random.normal(loc=mean_return, scale=volatility, size=(num_simulations, days))
    # Compute price paths: cumulative product of (1 + returns)
    price_paths = (1 + returns).cumprod(axis=1)
    # Final balances
    final_balances = initial_balance * price_paths[:, -1]
    # Statistics
    mean_final = np.mean(final_balances)
    median_final = np.median(final_balances)
    pct_5 = np.percentile(final_balances, 5)
    pct_95 = np.percentile(final_balances, 95)
    prob_target = np.mean(final_balances >= initial_balance * (1 + mean_return))
    return {
        "simulations": num_simulations,
        "days": days,
        "mean_final_balance": float(mean_final),
        "median_final_balance": float(median_final),
        "5th_percentile": float(pct_5),
        "95th_percentile": float(pct_95),
        "prob_exceed_target": float(prob_target)

"""
# [AUTO-FIXED] }