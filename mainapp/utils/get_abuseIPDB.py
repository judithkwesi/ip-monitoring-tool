import requests
import json
from decouple import config

API_Key = config('AbuseIPDB_API_Key')

def make_abuseipdb_request():
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        "Accept": "application/json",
        "Key": API_Key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        extract_to_file(data)
        return True
    else:
        print("Request failed with status code:", response.status_code)
        return None

def extract_to_file(data):
    # Extract IP addresses and write to a file
    with open('./mainapp/sites/abuseIPDB.txt', 'w') as file:
        for entry in data['data']:
            ip_address = entry['ipAddress']
            file.write(ip_address + '\n')

    print("IP addresses written to abuseIPDB.txt")