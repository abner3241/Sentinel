from utils.performance_analysis import PerformanceAnalyzer
from pathlib import Path

def main():
    analyzer = PerformanceAnalyzer(Path("signals.json"))
    report = analyzer.generate_report()
    print("Drawdown report (from performance output):")
    print(report)

if __name__ == "__main__":
    main()
