"""Run the existing opportunity detector with synthetic, offline market data."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.funding_arbitrage import FundingArbitrage


# These values are illustrative fixtures, not quotes or historical observations.
SCENARIOS = {
    "BTC": {"spot": 60000.0, "swap": 60030.0, "funding": 0.0002},
    "ETH": {"spot": 3000.0, "swap": 3020.0, "funding": 0.00005},
    "SOL": {"spot": 150.0, "swap": 155.0, "funding": 0.0002},
}


class SyntheticMarket:
    """Supply fixed prices and funding rates through the existing client interface."""

    def get_ticker(self, inst_id):
        pair = inst_id.split("-")[0]
        field = "swap" if inst_id.endswith("-SWAP") else "spot"
        return SCENARIOS[pair][field]

    def get_funding_rate(self, inst_id):
        return SCENARIOS[inst_id.split("-")[0]]["funding"]


def main():
    config = {
        "funding_threshold": 0.0001,
        "spread_threshold": 10.0,
        "check_interval": 60,
        "trading_pairs": list(SCENARIOS),
    }
    strategy = FundingArbitrage(config, exchange=SyntheticMarket())

    print("OFFLINE DEMO | synthetic data | no API keys | no orders")
    print("Signal: funding > 0.0100% AND swap - spot > 10.00 USDT")
    print()
    print(f"{'Pair':<6}{'Spot (USDT)':>14}{'Swap (USDT)':>14}"
          f"{'Funding':>12}{'Spread':>12}{'Signal':>9}")
    for pair, quote in SCENARIOS.items():
        signal = strategy.check_arbitrage_opportunity(pair)
        spread = quote["swap"] - quote["spot"]
        print(f"{pair:<6}{quote['spot']:>14.2f}{quote['swap']:>14.2f}"
              f"{quote['funding']:>11.4%}{spread:>13.2f}"
              f"{'YES' if signal else 'NO':>9}")
    print()
    print("A signal passes two thresholds; it is not a net-profit estimate.")


if __name__ == "__main__":
    main()
