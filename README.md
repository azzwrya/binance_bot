# Binance Futures Testnet Trading Bot 🚀

## 📖 What This Is
This is a professional-grade, interactive Python command-line application designed to interface securely with the **Binance Futures Testnet (USDT-M)**. It acts as a simulated trading environment gateway, allowing users to execute real-time trades using testnet funds without risking actual capital.

## ⚙️ What It Does
* **Interactive CLI Wizard:** Bypasses complex command-line arguments by providing a step-by-step interactive menu that guides the user through placing a trade.
* **Executes Trades:** Supports placing both **MARKET** and **LIMIT** orders for both **BUY** and **SELL** sides.
* **Validates Input:** Catches human errors (like typing letters instead of numbers, or negative quantities) before they are sent to the exchange.
* **Dual-Stream Logging:** Separates clean, human-readable order summaries from raw, detailed API payloads, recording both securely to a permanent log file (`bot_activity.log`).

## 🧠 How It Works (Project Structure)
The application strictly follows a separation-of-concerns architecture:

1. **The UI Layer (`cli.py`):** Handles all human interaction. It prompts the user for input, validates the data, formats the terminal output, and asks for execution confirmation.
2. **The API Layer (`bot/client.py`):** Acts as the "kitchen." It takes the validated instructions from the UI layer, securely signs the request using the `python-binance` library, and communicates with the Binance servers. 
3. **The Logging Layer (`bot/logging_config.py`):** Acts as the "black box." It captures both the raw JSON data sent to/from Binance and the formatted UI summaries, writing them to a file for auditing.
4. **The Security Layer (`.env`):** API keys are loaded exclusively through environment variables via `python-dotenv` to ensure secrets are never hardcoded.

## 🛠️ Setup Steps

### 1. Prerequisites
* **Python 3.7+** installed on your machine.
* A registered account on the [Binance Futures Testnet](https://testnet.binancefuture.com/).

### 2. Installation
Clone the repository or extract the project folder, then navigate to the directory in your terminal:
```bash
cd binance_bot
```

Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a file named exactly `.env` in the root directory of the project. Add your API credentials generated from the Binance Testnet dashboard:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
```
*(Note: Ensure you have clicked the "Faucet" button on the Testnet dashboard to add simulated USDT to your account before trading).*

## 🚀 How to Run It
Start the interactive wizard by running the following command in your terminal:
```bash
python cli.py
```

The bot will launch and guide you through the process:
* **Symbol:** Enter the trading pair (Defaults to `BTCUSDT`).
* **Side:** Type `BUY` or `SELL`.
* **Type:** Type `MARKET` or `LIMIT`.
* **Quantity:** Enter the amount to trade (must be > 0).
* **Price:** If using a Limit order, enter your target price.
* **Confirm:** Review the generated order summary and type `Y` to execute the trade on the network.

## 📋 Assumptions & Design Choices
* **Time In Force:** All `LIMIT` orders are hardcoded with a `GTC` (Good Till Cancelled) rule, as it is the most standard behavior for baseline limit testing.
* **Testnet Exclusivity:** The bot forcefully overrides the standard Binance base URL to `https://testnet.binancefuture.com/fapi/v1` to prevent any accidental mainnet executions.
* **Logging Priorities:** `force=True` is applied to the logging configuration to ensure the custom `bot_activity.log` file takes precedence over any third-party library logging hijacks.
