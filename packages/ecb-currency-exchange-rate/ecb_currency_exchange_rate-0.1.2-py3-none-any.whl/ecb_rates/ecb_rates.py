import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

namespaces = {'xmlns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
xml_file = 'eurofxref-hist.xml'
ecb_hist_rate_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'


def fetch_rates():
    """
    Downloads the latest historical exchange rate data from the ECB and saves it to a local file.
    """
    logging.info(f"Downloading {xml_file}...")
    try:
        response = requests.get(ecb_hist_rate_url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)

        with open(xml_file, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        logging.info(f"Downloaded and replaced {xml_file} successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to download {xml_file}. Error: {e}")


def update_historical_rates(xml_file):
    """
    Updates the historical rates if today's exchange rate is not already present.
    Fetches new data if necessary.

    :param xml_file: Path to the historical ECB XML file.
    """
    today_str = datetime.today().strftime("%Y-%m-%d")
    
    try:
        hist_tree = ET.parse(xml_file)
        hist_root = hist_tree.getroot()
        
        available_dates = sorted(
            [cube.attrib['time'] for cube in hist_root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces)],
            reverse=True
        )

        if today_str not in available_dates:
            logging.info("Today's exchange rate not found. Fetching new rate file.")
            fetch_rates()
        else:
            logging.info("Exchange rates are up to date.")
    except FileNotFoundError:
        logging.warning(f"File {xml_file} not found. Attempting to fetch data.")
        fetch_rates()
    except ET.ParseError:
        logging.error(f"Error parsing the XML file {xml_file}. Please check the file integrity.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while updating historical rates: {e}")


def get_exchange_rate(date, from_currency, to_currency):
    """
    Retrieves the exchange rate for the given date and currencies from the ECB historical XML file.
    If the date falls on a weekend or holiday, it uses the last available rate.

    :param date: Date in 'YYYY-MM-DD' format.
    :param from_currency: The base currency (e.g., 'USD').
    :param to_currency: The target currency (e.g., 'EUR').
    :return: Exchange rate as a float or None if not found.
    """
    update_historical_rates(xml_file)

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Convert date to datetime format
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        available_dates = sorted(
            [cube.attrib['time'] for cube in root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces)],
            reverse=True
        )
        
        while date_obj.strftime("%Y-%m-%d") not in available_dates:
            date_obj -= timedelta(days=1)  # Move to the previous day
        
        date_str = date_obj.strftime("%Y-%m-%d")

        for cube_time in root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces):
            if cube_time.attrib['time'] == date_str:
                rates = {rate.attrib['currency']: float(rate.attrib['rate']) for rate in cube_time.findall("xmlns:Cube", namespaces)}

                if from_currency == 'EUR':
                    return rates.get(to_currency)  # Return rate directly if from EUR
                elif to_currency == 'EUR':
                    return 1 / rates.get(from_currency) if rates.get(from_currency) else None
                elif from_currency in rates and to_currency in rates:
                    return rates[to_currency] / rates[from_currency]  # Cross-rate conversion

        logging.warning(f"Exchange rate for {from_currency} to {to_currency} on {date_str} not found.")
        return None

    except FileNotFoundError:
        logging.error(f"{xml_file} not found. Please fetch the latest data first.")
    except ET.ParseError:
        logging.error(f"Error parsing the XML file {xml_file}. Please check the file integrity.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while retrieving the exchange rate: {e}")
    
    return None  # Return None if no rate found or an error occurs
