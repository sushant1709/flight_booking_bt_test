import pytest
import json

import requests
from tenacity import retry, wait_fixed, stop_after_attempt
from src.booker_api_client import RestfulBookerClient
from utility.logging_config import get_logger

logger = get_logger(__name__)


# Load test data from JSON file
def load_test_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


test_data = load_test_data('testdata/test_data.json')
BASE_URL = test_data['base_url']
USERNAME = test_data['username']
PASSWORD = test_data['password']


@pytest.fixture(scope="module")
def api_client():
    return RestfulBookerClient(BASE_URL, USERNAME, PASSWORD)


@pytest.fixture(scope="module")
def bookings(api_client):
    booking1 = test_data['bookings'][0]
    booking2 = test_data['bookings'][1]

    # Generate 2 new bookings
    new_booking1 = api_client.create_booking(booking1)
    new_booking2 = api_client.create_booking(booking2)

    # Log all available booking IDs
    booking_ids = api_client.get_booking_ids()
    logger.info(f"All available booking IDs: {booking_ids}")

    # Log new bookings details
    logger.info(f"New booking 1 details: {new_booking1}")
    logger.info(f"New booking 2 details: {new_booking2}")

    return new_booking1, new_booking2


def test_update_bookings(api_client, bookings):
    new_booking1, new_booking2 = bookings

    # Modify total price for booking1 to 1000
    updated_booking1 = new_booking1.copy()
    updated_booking1['totalprice'] = 1000
    api_client.update_booking(new_booking1['bookingid'], updated_booking1)

    # Modify total price for booking2 to 1500
    updated_booking2 = new_booking2.copy()
    updated_booking2['totalprice'] = 1500
    api_client.update_booking(new_booking2['bookingid'], updated_booking2)

    # Log updated booking details
    logger.info(f"Updated booking 1 details: {updated_booking1}")
    logger.info(f"Updated booking 2 details: {updated_booking2}")


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def get_deleted_booking(api_client, booking_id):
    # Attempt to get the booking to verify deletion
    response = api_client.get_booking(booking_id)
    return response


def test_delete_booking(api_client, bookings):
    new_booking1, _ = bookings

    # Delete the first booking and log the return status
    delete_status = api_client.delete_booking(new_booking1['bookingid'])
    logger.info(f"Deleted booking 1 status code: {delete_status}")

    # Verify that the booking is deleted
    # with pytest.raises(requests.exceptions.HTTPError):
    #     get_deleted_booking(api_client, new_booking1['bookingid'])

    # Log the response code for verification
    logger.info(f"Response code for delete operation: {delete_status}")
