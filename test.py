import requests

def get_exchange_rates():
    url = 'http://api.nbp.pl/api/exchangerates/tables/A/'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        data = response.json()
        
        if 'rates' in data[0]:
            rates = data[0]['rates']
            return {rate['code']: rate['mid'] for rate in rates}
        else:
            raise ValueError("Unexpected API response structure")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

if __name__ == "__main__":
    exchange_rates = get_exchange_rates()
    if exchange_rates:
        for currency, rate in exchange_rates.items():
            print(f"{currency}: {rate}")