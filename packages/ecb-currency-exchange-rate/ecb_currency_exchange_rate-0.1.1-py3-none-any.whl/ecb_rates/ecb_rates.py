import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests

namespaces = {'xmlns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
xml_file = 'eurofxref-hist.xml'
ecb_hist_rate_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'


def fetch_rates():
    print(f"Downloading {xml_file}...")
    response = requests.get(ecb_hist_rate_url, stream=True)
    
    if response.status_code == 200:
        with open(xml_file, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded and replaced {xml_file} successfully.")
    else:
        print(f"Failed to download {xml_file}. HTTP Status: {response.status_code}")
    
        

def update_historical_rates(xml_file):
    """
    Fetches the latest daily exchange rate XML file from ECB and updates the historical XML file
    if today's exchange rate is not already present.
    
    :param xml_file: Path to the historical ECB XML file.
    """

    today_str = datetime.today().strftime("%Y-%m-%d")
    hist_tree = ET.parse(xml_file)
    hist_root = hist_tree.getroot()
    
    # Find the closest available date (last available rate if weekend or holiday)
    available_dates = sorted(
        [cube.attrib['time'] for cube in hist_root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces)],
        reverse=True
    )
    
    if today_str not in available_dates:
        print("fetch new rate file")
        fetch_rates()
    else:
        print("Exchange rate up to date!")
        return

def get_exchange_rate(date, from_currency, to_currency):
    """
    Fetches the exchange rate for a given date, from_currency, and to_currency from the ECB historical XML file.
    If the date falls on a weekend or holiday, it uses the last available rate.
    
    :param xml_file: Path to the downloaded ECB historical XML file.
    :param date: Date in 'YYYY-MM-DD' format.
    :param from_currency: The base currency (e.g., 'USD').
    :param to_currency: The target currency (e.g., 'EUR').
    :return: Exchange rate as a float or None if not found.
    """
    update_historical_rates(xml_file)
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
        
    # Convert date to datetime format
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    # Find the closest available date (last available rate if weekend or holiday)
    available_dates = sorted(
        [cube.attrib['time'] for cube in root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces)],
        reverse=True
    )
    
    while date_obj.strftime("%Y-%m-%d") not in available_dates:
        date_obj -= timedelta(days=1)  # Move to the previous day
    
    date_str = date_obj.strftime("%Y-%m-%d")
    
    # Find the matching date element
    for cube_time in root.findall(".//xmlns:Cube/xmlns:Cube[@time]", namespaces):
        if cube_time.attrib['time'] == date_str:
            rates = {rate.attrib['currency']: float(rate.attrib['rate']) for rate in cube_time.findall("xmlns:Cube", namespaces)}
            
            if from_currency == 'EUR':
                return rates.get(to_currency, None)  # Direct rate if from EUR
            elif to_currency == 'EUR':
                return 1 / rates.get(from_currency, None) if rates.get(from_currency) else None
            elif from_currency in rates and to_currency in rates:
                return rates[to_currency] / rates[from_currency]  # Cross rate conversion
    
    return None  # Return None if date or currency is not found
