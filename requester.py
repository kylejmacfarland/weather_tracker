import requests

class Requester:

    def __init__(self):
       return

    def request(self, latitude, longitude):
        headers = {"User-Agent": "weathertracker"}
        url = f"https://api.weather.gov/points/{latitude},{longitude}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except HTTPError:
            print(f"HTTP Error: {response.status_code}")
        except Timeout:
            print("Request timed out.")
        except RequestException:
            print("Request exception.")
        return {}
