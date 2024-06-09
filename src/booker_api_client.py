import requests
from utility.logging_config import get_logger

logger = get_logger(__name__)


class RestfulBookerClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = self.generate_token(username, password)

    def generate_token(self, username, password):
        url = f"{self.base_url}/auth"
        response = self.session.post(url, json={"username": username, "password": password})
        response.raise_for_status()
        token = response.json()['token']
        logger.info(f"Generated auth token: {token}")
        return token

    def create_booking(self, booking_data):
        url = f"{self.base_url}/booking"
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.session.post(url, json=booking_data, headers=headers)
        response.raise_for_status()
        logger.info(f"Created booking: {response.json()}")
        return response.json()

    def get_booking(self, booking_id):
        url = f"{self.base_url}/booking/{booking_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_booking_ids(self):
        url = f"{self.base_url}/booking"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def update_booking(self, booking_id, booking_data):
        url = f"{self.base_url}/booking/{booking_id}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        response = self.session.put(url, headers=headers, json=booking_data)
        response.raise_for_status()
        logger.info(f"Updated booking {booking_id}: {response.json()}")
        return response.json()

    def delete_booking(self, booking_id):
        url = f"{self.base_url}/booking/{booking_id}"
        headers = {'Authorization': f'Basic {self.token}'}
        response = self.session.delete(url, headers=headers)
        # response.raise_for_status()
        # logger.info(f"Deleted booking {booking_id}")
        return response.status_code
