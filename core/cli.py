import argparse
from utils.pyramiding import calculate_pyramiding_targets
from utils.trailing_stop import trailing_stop_vwap, compute_vwap, compute_pivots
from utils.order_flow import compute_candle_delta
from utils.hedge_strategies import hedge_market_neutral, grid_strategy

def main():
    parser = argparse.ArgumentParser(description="CriptoSentinel CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Start
    p_start = subparsers.add_parser('start', help='Start the API and bot')
    p_start.set_defaults(func=lambda args: print("Starting CriptoSentinel..."))

    # Backtest
    p_bt = subparsers.add_parser('backtest', help='Run backtest')
    p_bt.set_defaults(func=lambda args: print("Running backtest..."))

    # Gen gRPC
    p_grpc = subparsers.add_parser('gen-grpc', help='Generate gRPC code')
    p_grpc.set_defaults(func=lambda args: print("Generating gRPC..."))

    # Run
    p_run = subparsers.add_parser('run', help='Run application')
    p_run.set_defaults(func=lambda args: print("Running application..."))

    # Pyramiding
    p_py = subparsers.add_parser('pyramiding', help='Calcula níveis de pyramiding')
    p_py.add_argument('--entry', type=float, required=True, help='Preço de entrada')
    p_py.add_argument('--size', type=float, default=1.0, help='Tamanho de posição')
    p_py.set_defaults(func=lambda args: print(calculate_pyramiding_targets(args.entry, [0.005,0.015,0.03], args.size)))

    # Trailing Stop
    p_ts = subparsers.add_parser('trailing-stop', help='Calcula trailing stop VWAP/Pivots')
    p_ts.add_argument('--symbol', required=True)
    p_ts.add_argument('--side', choices=['buy','sell'], required=True)
    p_ts.add_argument('--offset', type=float, default=0.005)
    p_ts.set_defaults(func=lambda args: print({
        'vwap': compute_vwap(args.symbol),
        'stop': trailing_stop_vwap(args.symbol, args.side, args.offset),
        'pivots': compute_pivots(args.symbol)
    }))

    # Candle Delta
    p_cd = subparsers.add_parser('candle-delta', help='Calcula delta de candle')
    p_cd.add_argument('--symbol', required=True)
    p_cd.add_argument('--limit', type=int, default=200)
    p_cd.set_defaults(func=lambda args: print({'delta': compute_candle_delta(args.symbol, args.limit)}))

    # Hedge
    p_h = subparsers.add_parser('hedge', help='Hedge market-neutral')
    p_h.add_argument('symbol1', help='Símbolo 1')
    p_h.add_argument('symbol2', help='Símbolo 2')
    p_h.add_argument('size', type=float, help='Tamanho de posição')
    p_h.set_defaults(func=lambda args: print(hedge_market_neutral(args.symbol1, args.symbol2, args.size)))

    # Grid
    p_g = subparsers.add_parser('grid', help='Grid trading')
    p_g.add_argument('symbol', help='Símbolo')
    p_g.add_argument('lower', type=float, help='Preço mínimo')
    p_g.add_argument('upper', type=float, help='Preço máximo')
    p_g.add_argument('--levels', type=int, default=5)
    p_g.add_argument('--size', type=float, default=1.0)
    p_g.set_defaults(func=lambda args: print(grid_strategy(args.symbol, args.lower, args.upper, levels=args.levels, size=args.size)))

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
