#!/usr/bin/env python3

import os
import time
import yfinance as yf
import datetime

print("=== macOS Stock Monitor (Native Notifications) ===")

# Stock configuration - Updated with current realistic limits
tickers = ["AAPL", "SPY", "MSCI", "META", "GOOGL", "BRK-B", "RHM.DE", "MSFT", "AMZN", "PDD", "BABA"]
real_names = [
    "Apple",
    "S&P 500",
    "MSCI World",
    "Meta Platforms",
    "Alphabet",
    "Berkshire Hathaway",
    "Rheinmetall AG",
    "Microsoft",
    "Amazon",
    "Pinduoduo",
    "Alibaba"
]
upper_limit = [250.00, 650.00, 520.00, 750.00, 200.00, 520.00, 1600.00, 500.00, 250.00, 160.00, 150.00]
lower_limit = [200.00, 450.00, 400.00, 400.00, 150.00, 400.00, 1200.00, 400.00, 180.00, 100.00, 90.00]

# Track notifications
notification_sent = {ticker: {"upper": False, "lower": False} for ticker in tickers}

def get_stock_price(ticker):
    """Get current stock price using yfinance"""
    print(f"Fetching price for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            price = data['Close'].iloc[-1]
            print(f"✓ {ticker}: ${price:.2f}")
            return price
        else:
            print(f"✗ No data available for {ticker}")
            return None
    except Exception as e:
        print(f"✗ Error fetching data for {ticker}: {e}")
        return None

def send_macos_notification(title, message):
    """Send notification using macOS native osascript"""
    print(f"🔔 Sending notification: {title}")
    try:
        # Escape quotes in the message
        title_escaped = title.replace('"', '\\"')
        message_escaped = message.replace('"', '\\"')
        
        # Use osascript to send native macOS notification
        command = f'osascript -e \'display notification "{message_escaped}" with title "{title_escaped}" sound name "Glass"\''
        
        result = os.system(command)
        if result == 0:
            print(f"✅ Notification sent successfully: {title}")
        else:
            print(f"❌ Failed to send notification (error code: {result})")
            
    except Exception as e:
        print(f"❌ Error sending notification: {e}")

def check_stock_prices():
    """Check all stock prices and send alerts if needed"""
    print(f"\n📊 Checking prices at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for i, ticker in enumerate(tickers):
        current_price = get_stock_price(ticker)
        
        if current_price is None:
            continue
            
        print(f"📈 {ticker}: ${current_price:.2f} (Range: ${lower_limit[i]:.2f} - ${upper_limit[i]:.2f})")
        
        # Check upper limit
        if current_price > upper_limit[i] and not notification_sent[ticker]["upper"]:
            title = f"🚨 {ticker} SELL ALERT!"
            message = f"{real_names[i]} is at ${current_price:.2f} (above ${upper_limit[i]:.2f}). Consider selling! 📈"

            send_macos_notification(title, message)
            
            notification_sent[ticker]["upper"] = True
            notification_sent[ticker]["lower"] = False
            
        # Check lower limit
        elif current_price < lower_limit[i] and not notification_sent[ticker]["lower"]:
            title = f"💰 {ticker} BUY ALERT!"
            message = f"{real_names} is at ${current_price:.2f} (below ${lower_limit[i]:.2f}). Consider buying! 📉"
            
            send_macos_notification(title, message)
            
            notification_sent[ticker]["lower"] = True
            notification_sent[ticker]["upper"] = False
            
        # Reset flags if price is back within range
        elif lower_limit[i] <= current_price <= upper_limit[i]:
            notification_sent[ticker]["upper"] = False
            notification_sent[ticker]["lower"] = False

def main():
    """Main function"""
    print("🚀 Stock Price Monitor Started!")
    print("📋 Monitoring stocks:")
    for i, ticker in enumerate(tickers):
        print(f"   {ticker}: ${lower_limit[i]:.2f} - ${upper_limit[i]:.2f}")
    
    print("\n🔔 This version uses macOS native notifications with sound!")
    print("⏹️  Press Ctrl+C to stop\n")
    
    print("\n⏰ Starting monitoring in 3 seconds...")
    time.sleep(3)
    
    try:
        while True:
            check_stock_prices()
            print("⏳ Waiting 5 seconds...")
            for i in range(5, 0, -1):
                print(f"\r⏱️  Next check in {i} seconds... (Ctrl+C to stop)", end="", flush=True)
                time.sleep(1)
            print()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stock monitor stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
