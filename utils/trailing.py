def calculate_trailing_stop(highest_price: float, trailing_pct: float) -> float:
# [AUTO-FIXED]     Calcula o preço de stop com base no maior preço alcançado e percentual de trailing.
# [AUTO-FIXED]     :param highest_price: maior preço atingido desde a entrada
# [AUTO-FIXED]     :param trailing_pct: percentual de trailing (ex.: 0.02 para 2%)
# [AUTO-FIXED]     :return: preço de stop
    if trailing_pct < 0 or trailing_pct > 1:
        raise ValueError("Trailing percentage must be between 0 and 1")
    return highest_price * (1 - trailing_pct)
