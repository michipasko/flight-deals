class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(
            self,
            record_id,
            city,
            iata_code,
            lowest_price,
    ):
        self.record_id = record_id
        self.city = city
        self.iata_code = iata_code
        self.lowest_price = lowest_price
        self.cheapest_flight = None
