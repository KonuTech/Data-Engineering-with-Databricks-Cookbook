import requests
from datetime import date, timedelta
import logging

# Configure logging to display timestamps, log levels, and messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL for fetching exchange rates of a specific currency from the NBP API
NBP_API_URL = "http://api.nbp.pl/api/exchangerates/rates/A/{}/?format=json"

def fetch_exchange_rate(currency_code: str, request_date: date):
    """Fetch exchange rate for a specific currency and date from the NBP API."""
    url = NBP_API_URL.format(currency_code)
    logging.info(f"Fetching exchange rate for {currency_code} on {request_date} from {url}")
    try:
        response = requests.get(url)
        logging.debug(f"Response status code: {response.status_code}")
        
        if response.status_code == 404:
            logging.warning(f"No data available for {currency_code} on {request_date} (404 Not Found). Trying previous available date.")
            return None
        
        response.raise_for_status()
        logging.info(f"Successfully fetched data for {currency_code} on {request_date}")
        return response.json()
    except requests.ConnectionError as e:
        logging.error(f"Network error while fetching data for {currency_code} on {request_date}: {e}")
        return None
    except requests.RequestException as e:
        logging.error(f"Error fetching data from NBP API for {currency_code} on {request_date}: {e}")
        return None

def process_exchange_rate(currency_code: str):
    """Fetch exchange rate for a specific currency and the most recent available date."""
    today = date.today()
    max_days_back = 5  # Attempt fetching data up to 5 days back if not available
    
    request_date = today
    logging.info(f"Processing data for {currency_code} on {request_date}")
    
    rates_data = fetch_exchange_rate(currency_code, request_date)
    attempts = 0
    while rates_data is None and attempts < max_days_back:
        request_date -= timedelta(days=1)
        logging.info(f"Retrying with previous date: {request_date}")
        rates_data = fetch_exchange_rate(currency_code, request_date)
        attempts += 1
    
    if rates_data:
        logging.info(f"Fetched exchange rate for {currency_code} on {request_date}: {rates_data['rates'][0]['mid']}")
    else:
        logging.warning(f"No exchange rate data available after {max_days_back} attempts.")

if __name__ == "__main__":
    currency = "USD"  # Change this to any currency code as needed
    logging.info(f"Starting exchange rate processing script for {currency}.")
    process_exchange_rate(currency)
    logging.info("Exchange rate processing completed.")
