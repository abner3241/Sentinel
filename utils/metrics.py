from prometheus_client import CollectorRegistry, Counter, Gauge

registry = CollectorRegistry()
ORDER_COUNTER = Counter('order_counter', 'Number of orders', registry=registry)
ORDER_LATENCY = Gauge('order_latency', 'Order latency ms', registry=registry)
PNL_GAUGE = Gauge('pnl_gauge', 'PnL gauge', registry=registry)
