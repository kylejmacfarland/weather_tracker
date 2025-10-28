import requests

class Requester:

    def __init__(self):
       return

    def request(self, uri):
        url = f"https://api.weather.gov/{uri}"
        return self.request_url(url)

    def request_url(self, url):
        headers = {"User-Agent": "weathertracker"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            print(f"HTTP Error: {response.status_code}")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException:
            print("Request exception.")
        return {}
