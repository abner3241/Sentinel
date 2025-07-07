
class DryRunClient:
    def __init__(self):
        self.orders = []
        self.balance = 100000.0

    def __init__(self):
        self.orders = []

    async def place_order(self, symbol: str, side: str, qty: float, price: float = None, order_type: str = "Market"):
        order = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "order_type": order_type,
# [AUTO-FIXED]             "status": "filled"
# [AUTO-FIXED]         self.orders.append(order)
# [AUTO-FIXED]         return order

# [AUTO-FIXED]     async def get_open_orders(self, symbol: str = None):
# [AUTO-FIXED]         return self.orders


# [AUTO-FIXED] async def get_balance(self):
# [AUTO-FIXED]     """Retorna o saldo simulado."""
    # Dry run mantém saldo hipotético
# [AUTO-FIXED]     return getattr(self, 'balance', None)
}