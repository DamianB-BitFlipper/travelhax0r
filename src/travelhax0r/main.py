from fast_flights import FlightData, Passengers, TFSData, get_flights_from_filter


def main():
    result = get_flights_from_filter(
        TFSData.from_interface(
            flight_data=[
                FlightData(date="2025-12-12", from_airport="BER", to_airport="MCO"),
                FlightData(date="2026-01-12", from_airport="MCO", to_airport="BER"),
            ],
            trip="round-trip",
            seat="economy",
            passengers=Passengers(
                adults=1, children=0, infants_in_seat=0, infants_on_lap=0
            ),
        ),
        mode="local",
        currency="USD",
    )

    print(result)


if __name__ == "__main__":
    main()
