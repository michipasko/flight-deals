# Login: https://tequila.kiwi.com/portal/login
# Documentation Tequila Locations API: https://tequila.kiwi.com/portal/docs/tequila_api/locations_api
# Documentation Tequila Search API: https://tequila.kiwi.com/portal/docs/tequila_api/search_api

import dotenv
import os
import requests
from flight_data import FlightData

dotenv.load_dotenv()

API_KEY = os.getenv("TEQUILA_API_KEY")
API_BASE_URL = "https://tequila-api.kiwi.com"
SEARCH_ENDPOINT = "/v2/search"
LOCATION_ENDPOINT = "/locations/query"


class FlightSearch:
    def __init__(
            self,
            point_of_departure,
            date_from,
            date_to,
            min_nights_in_destination,
            max_nights_in_destination,
    ):
        self.point_of_deparature = point_of_departure
        self.date_from = date_from
        self.date_to = date_to
        self.min_nights_in_destination = min_nights_in_destination
        self.max_nights_in_destination = max_nights_in_destination

    @staticmethod
    def fetch_iata_code(city):
        request_header = {
            "apikey": API_KEY,
        }

        request_body = {
            "term": city,
            "location_types": "airport",
        }

        response = requests.get(
            url=f"{API_BASE_URL}{LOCATION_ENDPOINT}",
            headers=request_header,
            params=request_body
        )

        location_data = response.json()
        # print(location_data)

        iata_code = location_data["locations"][0]["city"]["code"]
        return iata_code

    def fetch_cheap_flights(self, flight_data: FlightData):
        request_header = {
            "apikey": API_KEY,
        }

        request_body = {
            "fly_from": self.point_of_deparature,
            "fly_to": flight_data.iata_code,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "nights_in_dst_from": self.min_nights_in_destination,
            "nights_in_dst_to": self.max_nights_in_destination,
            "price_to": flight_data.lowest_price
        }

        # This won't work:
        # response = requests.get(url=f"{API_BASE_URL}{SEARCH_ENDPOINT}", headers=request_header, json=request_body)
        response = requests.get(
            url=f"{API_BASE_URL}{SEARCH_ENDPOINT}",
            headers=request_header,
            params=request_body
        )

        data = response.json()
        print(data)
        #print(data)
        if len(data["data"]) > 0:
            cheapest_flight = self.get_cheapest_flight(
                flight_data_from_tequila=data
            )
            return cheapest_flight

    def get_cheapest_flight(self, flight_data_from_tequila):
        cheapest_price = None
        cheapest_flight = None
        for flight in flight_data_from_tequila["data"]:
            # print(flight)
            if cheapest_price is None or flight["price"] < cheapest_price:
                cheapest_price = flight["price"]
                cheapest_flight = flight
        return cheapest_flight
