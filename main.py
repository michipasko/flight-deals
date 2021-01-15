# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.

import datetime
from data_manager import DataManager
import dotenv
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os

dotenv.load_dotenv()

SHEETY_SHEET_ENDPOINT = "/3f3d85f59b2ca6abccdbf1cd23865997/flightDeals/prices"
POINT_OF_DEPARTURE = "BER"  # Your location.
MIN_NIGHTS_IN_DESTINATION = 7
MAX_NIGHTS_IN_DESTINATION = 14
DATE_FROM = datetime.date.today().strftime("%d/%m/%Y")
DATE_TO = (datetime.date.today() + datetime.timedelta(days=180)).strftime("%d/%m/%Y")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")


def main():
    print(f"Departure: {POINT_OF_DEPARTURE}")
    print(f"Date from: {DATE_FROM}")
    print(f"Date to: {DATE_TO}")

    # Here we load our preferred destinations from the provided google sheet.
    data_manager = DataManager(
        sheety_sheet_endpoint=SHEETY_SHEET_ENDPOINT
    )
    flight_data = data_manager.flight_data

    # Here we update our preferred destinations with IATA code if code is missing.
    updated_records = []
    for record in flight_data:
        if record.iata_code == "":
            iata_code = FlightSearch.fetch_iata_code(record.city)
            record.iata_code = iata_code
            updated_records.append(record)

    # print(updated_records)

    # Here we update our Google Sheets with the IATA Codes.
    data_manager.update_flight_data_with_iata_code(
        updated_records=updated_records
    )

    # Here we search for cheap flight.
    flight_searcher = FlightSearch(
        point_of_departure=POINT_OF_DEPARTURE,
        date_from=DATE_FROM,
        date_to=DATE_TO,
        min_nights_in_destination=MIN_NIGHTS_IN_DESTINATION,
        max_nights_in_destination=MAX_NIGHTS_IN_DESTINATION,
    )

    # Here we fetch the cheapest flights and send an SMS.
    for record in flight_data:
        record.cheapest_flight = flight_searcher.fetch_cheap_flights(record)
        if record.cheapest_flight is not None:
            NotificationManager.send_message(flight_data=record.cheapest_flight, message_to=MY_PHONE_NUMBER)


if __name__ == "__main__":
    main()
