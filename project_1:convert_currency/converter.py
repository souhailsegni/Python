import requests
from dotenv import load_dotenv
import os

load_dotenv()

def convert_currency(amount, from_currency, to_currency):
    # This is a mock conversion function. In a real application, you would use an API or a database.
    api_key = os.getenv("API_KEY")
    url=f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'conversion_result' in data:
            return data['conversion_result']
        else:
            raise ValueError("Conversion failed. Please check the currency codes.")
    else:
        raise ValueError(f"Error fetching conversion rate: {response.status_code} - {response.text}")