# Automated Binance Testnet Trading Interface

A structured, modular Python command-line interface (CLI) built to interact with the Binance API for executing and validating algorithmic trading orders. This system supports automated execution profiles (`MARKET` orders) and boundary-constrained execution parameters (`LIMIT` orders), complete with unified input validation, automated runtime log tracing, and an enhanced interactive setup wizard.

---

## Project Architecture

The application is structured cleanly using a modular layout to separate configuration, validation, networking, and execution layers:

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Marks directory as a Python package
│   ├── cli.py               # Handles terminal commands, arguments, and wizard menu
│   ├── client.py            # Manages API connection and request execution
│   ├── logging_config.py    # Configures unified file and console logging
│   ├── orders.py            # Builds and dispatches exchange order payloads
│   └── validators.py        # Enforces strict input validation constraints
├── logs/
│   └── trading_bot.log      # Persisted system execution traces
├── .env                     # Local environment security configuration (git-ignored)
└── requirements.txt         # Project dependencies

## Core System Features
1.Interactive CLI Wizard Mode (Bonus Feature Completed): Launching the bot without inline arguments automatically opens a guided terminal step selection wizard to pick and validate order metrics step-by-step.

2.Strict Input Validation: Prior to network dispatch, all data passes through specialized validation routines checking for valid asset pairing formats, non-zero volumes, and correct execution profiles.

3.Unified Event Logging: All system operations, outbound trade requests, and inbound exchange responses are logged automatically to logs/trading_bot.log for debugging and compliance.

##Architectural & Integration Assumptions
To ensure seamless code evaluation across varying network environments, the following systemic assumptions were implemented:

1.Validation Endpoint Targeting: The trading client utilizes the public Binance validation pipeline (/api/v3/order/test). This processes complete structural validation, request parameter integrity, and signature verification without hitting localized network IP restrictions or account permission locks.

2.Environment Isolation: The configuration assumes runtime isolation via an .env file for secure credential storage, keeping API configurations decoupled from the core execution logic.

3.Asset Scope Constraint: The verification logic assumes standard USDT-M pairs (such as BTCUSDT) are utilized for testing request structures.

#Installation & Setup
1.Install Dependencies: Ensure all framework components are installed locally within your workspace:
pip install -r requirements.txt

2.Environment Configuration: Confirm your .env file exists at the project root with your testing credentials:
BINANCE_API_KEY="your_api_key_here"
BINANCE_SECRET_KEY="your_secret_key_here"


##Verification & How to Run Examples
You can execute the interface using either standard raw command line parameters or the enhanced guided wizard:

1. Interactive Menu Wizard (Recommended / Bonus Mode)
Simply run the script with no arguments to trigger the interactive prompts:

**PowerShell (Windows):**

```bash
$env:PYTHONPATH='.'; python -m bot.cli
```

**macOS/Linux:**

```bash
PYTHONPATH=. python -m bot.cli
```

2. Market Order Example (Direct CLI)
Dispatches an immediate request execution against current market liquidity:

**PowerShell (Windows):**

```bash
$env:PYTHONPATH='.'; python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**macOS/Linux:**

```bash
PYTHONPATH=. python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

3. Limit Order Example (Direct CLI)
Places a constraint-driven order targeted at a specific price floor threshold:

**PowerShell (Windows):**

```bash
$env:PYTHONPATH='.'; python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 75000
```

**macOS/Linux:**

```bash
PYTHONPATH=. python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 75000
```

---

## Streamlit UI (Local)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the UI:

**PowerShell (Windows):**

```bash
$env:PYTHONPATH='.'; streamlit run ui/streamlit_app.py
```

**macOS/Linux:**

```bash
PYTHONPATH=. streamlit run ui/streamlit_app.py
```

This UI lets you place mock testnet orders and view `logs/trading_bot.log` live.

---

## Vercel (HTTP API)

This repo includes Vercel-compatible Python Functions under `api/`:

- `GET /api/health`
- `GET /api/order` (usage)
- `POST /api/order` (place order)

Example request body:

```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "MARKET",
  "quantity": 0.01
}
```
