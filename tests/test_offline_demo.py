"""Exercise signal boundaries and the credential-free onboarding path."""

import contextlib
import io
from pathlib import Path
import runpy
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from strategies.funding_arbitrage import FundingArbitrage


class MarketStub:
    def __init__(self, spot=60000.0, swap=60030.0, funding=0.0002):
        self.spot = spot
        self.swap = swap
        self.funding = funding

    def get_ticker(self, inst_id):
        return self.swap if inst_id.endswith("-SWAP") else self.spot

    def get_funding_rate(self, inst_id):
        return self.funding


class SignalTests(unittest.TestCase):
    def test_default_adapter_keeps_existing_configuration(self):
        module = ModuleType("exchange.okx_client")
        module.OKXClient = Mock()
        config = {
            "api_key": "",
            "api_secret": "",
            "passphrase": "",
            "is_test": True,
            "funding_threshold": 0.0001,
            "spread_threshold": 10.0,
            "check_interval": 60,
            "trading_pairs": ["BTC"],
        }
        with patch.dict(sys.modules, {"exchange.okx_client": module}):
            strategy = FundingArbitrage(config)
        module.OKXClient.assert_called_once_with("", "", "", True)
        self.assertIs(strategy.exchange, module.OKXClient.return_value)

    def signal(self, **quotes):
        config = {
            "funding_threshold": 0.0001,
            "spread_threshold": 10.0,
            "check_interval": 60,
            "trading_pairs": ["BTC"],
        }
        strategy = FundingArbitrage(config, exchange=MarketStub(**quotes))
        return strategy.check_arbitrage_opportunity("BTC")

    def test_both_thresholds_must_be_exceeded(self):
        self.assertTrue(self.signal())
        self.assertFalse(self.signal(funding=0.00005))
        self.assertFalse(self.signal(swap=60005.0))

    def test_threshold_equality_does_not_signal(self):
        self.assertFalse(self.signal(funding=0.0001))
        self.assertFalse(self.signal(swap=60010.0))

    def test_missing_market_data_does_not_signal(self):
        for quote in ("spot", "swap", "funding"):
            with self.subTest(quote=quote):
                self.assertFalse(self.signal(**{quote: None}))

    def test_zero_and_negative_funding_do_not_signal(self):
        self.assertFalse(self.signal(funding=0.0))
        self.assertFalse(self.signal(funding=-0.0002))

    def test_offline_demo_never_connects_or_executes_orders(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), \
                patch("socket.socket", side_effect=AssertionError("Network access")), \
                patch.object(FundingArbitrage, "execute_arbitrage",
                             side_effect=AssertionError("Execution path")):
            runpy.run_path(str(ROOT / "examples" / "demo.py"), run_name="__main__")
        report = output.getvalue()
        self.assertIn("synthetic data", report)
        signals = {
            row.split()[0]: row.split()[-1]
            for row in report.splitlines()
            if row.startswith(("BTC ", "ETH ", "SOL "))
        }
        self.assertEqual(signals, {"BTC": "YES", "ETH": "NO", "SOL": "NO"})


if __name__ == "__main__":
    unittest.main()
