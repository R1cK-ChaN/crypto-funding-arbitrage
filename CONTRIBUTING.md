# Contributing

Start with the offline demo to understand the detector without connecting an
exchange account. Small, reproducible improvements are welcome.

## Local checks

Use Python 3.10 or later from the repository root:

```bash
python3 -S examples/demo.py
python3 -S -m unittest discover -s tests -v
```

These commands need no installed packages or API keys. To work on the existing
HTTP monitor, use a virtual environment and install `requirements.txt` as described
in the README. Keep tests independent of live services and private accounts.

## Propose a change

1. Describe the observed problem and expected behavior in an issue or pull request.
2. Keep the change focused. For signal changes, include units and boundary cases.
3. Add a regression test for changed behavior using synthetic inputs.
4. Run the local checks and update the affected examples or documentation.
5. Include the commands and results in the pull request.

For bug reports, include your Python version, the command you ran, and a minimal
reproduction. Remove credentials, account identifiers, balances, and private
trading data from logs before sharing them.

## Useful areas to explore

- Instrument-specific funding intervals and normalized spread comparisons.
- A model that accounts for fees and slippage before calling a signal profitable.
- HTTP timeouts and explicit handling of exchange error responses.
- Deterministic tests for malformed and missing market data.

Order execution, balance-aware sizing, and backtesting are not implemented.
Discuss changes to those areas before extending the current prototype. Label
synthetic examples as synthetic, and include reproducible methodology for any
performance claims.
