# Google Sheet: https://docs.google.com/spreadsheets/d/1FvjFLqeZzMHhsqPic_Eo5SbH4-Pf6uc7pcYaTREFhHE/edit#gid=0

from flight_data import FlightData
import requests

SHEETY_BASE_URL = "https://api.sheety.co"


class DataManager:
    """This class is responsible for talking to a Google Sheets with destinations and price data."""

    def __init__(self, sheety_sheet_endpoint):
        self.sheety_sheet_endpoint = sheety_sheet_endpoint
        self.flight_data = self.fetch_flight_data_from_google_sheet()

    def fetch_flight_data_from_google_sheet(self) -> list[FlightData]:
        """This method will fetch the flight data of an user from an Google Sheet."""
        response = requests.get(
            url=f"{SHEETY_BASE_URL}{self.sheety_sheet_endpoint}"
        )
        response.raise_for_status()
        data = response.json()

        flight_data = [
            FlightData(
            record_id=destination["id"],
            city=destination["city"],
            iata_code=destination["iataCode"],
            lowest_price=destination["lowestPrice"]
            ) for destination in data["prices"]
        ]

        return flight_data

    def update_flight_data_with_iata_code(self, updated_records: list[FlightData]):
        for record in updated_records:
            request_headers = {
                "Content-Type": "application/json"
            }

            request_body = {
                "price": {
                    "iataCode": record.iata_code
                }
            }

            response = requests.put(
                url=f"{SHEETY_BASE_URL}{self.sheety_sheet_endpoint}/{record.record_id}",
                headers=request_headers,
                json=request_body,
            )
            response.raise_for_status()
            # print(response.text)
