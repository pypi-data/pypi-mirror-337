import requests
import sys

API_URL = "https://api.etherscan.io/api"
API_KEY = "XTPAQIEJFAEJ1B65XQY3J8UDC49S4B6MKC"  # Replace with your actual key

def get_gas_price():
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": API_KEY,
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "1":
            result = data["result"]
            print(f"💨 Gas Prices (Gwei):")
            print(f"  - Safe: {result['SafeGasPrice']}")
            print(f"  - Propose: {result['ProposeGasPrice']}")
            print(f"  - Fast: {result['FastGasPrice']}")
        else:
            print("⚠️  Error:", data["message"])
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: ether-gas-price-server")
        print("A simple CLI tool to fetch Ethereum gas prices.")
    else:
        get_gas_price()

if __name__ == "__main__":
    main()

