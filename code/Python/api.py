import requests
import json
import colorama
from colorama import Fore, Style
import humanize

def make_rest_request():
    url = "https://api.magicthegathering.io/v1/formats"  # Example URL

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse JSON response
        data = response.json()
        formatted_data = json.dumps(data, indent=4, sort_keys=True)  # Format JSON response
        print("Response received:")
        # print(formatted_data)
        print(Fore.LIGHTGREEN_EX + formatted_data)
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

if __name__ == "__main__":
    make_rest_request()
