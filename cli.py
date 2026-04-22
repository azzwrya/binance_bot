import os
import logging
from dotenv import load_dotenv
from bot.client import BinanceTestnetClient
from bot.logging_config import setup_logging

# Load environment variables and start logging
load_dotenv()
setup_logging()

# Create a logger specifically for the CLI interface
cli_logger = logging.getLogger("bot.cli")

# --- VALIDATION HELPERS ---
def get_valid_float(prompt_text):
    while True:
        try:
            value = float(input(prompt_text))
            if value <= 0:
                print("  ⚠️ Value must be greater than 0. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠️ Invalid input. Please enter a number.")

def get_valid_choice(prompt_text, valid_choices):
    while True:
        choice = input(prompt_text).strip().upper()
        if choice in valid_choices:
            return choice
        print(f"  ⚠️ Invalid choice. Please type one of: {', '.join(valid_choices)}")

# --- MAIN MENU WIZARD ---
def main_menu():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("❌ Error: API credentials missing in .env file.")
        return

    bot = BinanceTestnetClient(api_key, api_secret)

    while True:
        print("\n" + "="*45)
        print(" 🚀 BINANCE FUTURES INTERACTIVE BOT 🚀 ")
        print("="*45)

        symbol = input("Enter Symbol (Default: BTCUSDT): ").strip().upper()
        if not symbol:
            symbol = "BTCUSDT" 

        side = get_valid_choice("Select Side (BUY / SELL): ", ["BUY", "SELL"])
        order_type = get_valid_choice("Select Order Type (MARKET / LIMIT): ", ["MARKET", "LIMIT"])
        qty = get_valid_float(f"Enter Quantity for {symbol}: ")
        
        price = None
        if order_type == "LIMIT":
            price = get_valid_float(f"Enter Limit Price for {symbol}: ")

        print("\n" + "-"*30)
        print(" 📋 ORDER CONFIRMATION ")
        print("-"*30)
        print(f"Action:   {side} {qty} {symbol}")
        print(f"Type:     {order_type}")
        if price:
            print(f"Price:    ${price}")
        print("-"*30)
        
        confirm = get_valid_choice("Execute this trade? (Y/N): ", ["Y", "N"])
        
        if confirm == "Y":
            print("\n⏳ Sending order to Binance Testnet...")
            try:
                # 1. Send the order (client.py logs the raw data here)
                res = bot.place_futures_order(symbol, side, order_type, qty, price)
                
                # 2. Print human-readable summary to the screen
                print("✅ ORDER SUCCESSFUL ✅")
                print(f"Order ID:     {res.get('orderId')}")
                print(f"Status:       {res.get('status')}")
                
                # 3. Log human-readable summary to the bot_activity.log file!
                cli_logger.info(f"--- UI SUMMARY: {side} {qty} {symbol} | Type: {order_type} | ID: {res.get('orderId')} | Status: {res.get('status')} ---")
                
            except Exception:
                print("❌ ORDER FAILED ❌")
                print("Check 'bot_activity.log' for details.")
                cli_logger.error(f"--- UI SUMMARY: FAILED to execute {side} {qty} {symbol} ---")
        else:
            print("\n🚫 Order cancelled by user.")
            cli_logger.info("User cancelled order at confirmation screen.")

        again = get_valid_choice("\nPlace another order? (Y/N): ", ["Y", "N"])
        if again == "N":
            print("\nExiting bot. Goodbye! 👋\n")
            break

if __name__ == "__main__":
    main_menu()