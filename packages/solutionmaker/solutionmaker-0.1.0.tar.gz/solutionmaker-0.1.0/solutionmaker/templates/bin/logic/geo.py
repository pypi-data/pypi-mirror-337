import requests
from bin.settings.settings import logger

def get_nominatim_coordinates_latlon_fc(address, nominatim_url = "https://nominatim.openstreetmap.org/search"):
    latitude, longitude = 0, 0

    params = {"q": address, "format": "json", "addressdetails": 1}
    headers = {
        'User-Agent': 'NonameApp/1.0 (123@mymail.org)'  # Set own
    }

    try:
        response = requests.get(nominatim_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = data[0].get("lat")
            longitude = data[0].get("lon")
    except (requests.RequestException, ValueError) as e:
        logger.info(f"ER - in requestion coordinates for address '{address}': {e}")
    finally:
        return latitude, longitude