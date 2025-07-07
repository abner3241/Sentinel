def calculate_pyramiding_targets(entry_price: float,
                                levels: list = [0.005, 0.015, 0.03],
                                size: float = 1.0):
    """Gera níveis de preço e quantidades para execução parcial da posição.
    levels: frações de lucro alvo (e.g., 0.005 = 0.5%).
    Retorna lista de dicts: [{'price': ..., 'qty': ...}, ...]"""
    targets = []
    remaining = size
    part = size / len(levels)
    for pct in levels:
        price = entry_price * (1 + pct)
        qty = part
        targets.append({'price': price, 'qty': qty})
        remaining -= qty
    # Add remaining to last target
    if targets:
        targets[-1]['qty'] += remaining
    return targets
