import pandas as pd

def export_performance(signals_file, output_file):
    """Exporta métricas de performance para CSV."""
    df = pd.read_json(signals_file)
    df.to_csv(output_file, index=False)
