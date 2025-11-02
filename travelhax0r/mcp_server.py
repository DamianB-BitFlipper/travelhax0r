#!/usr/bin/env python3
"""
MCP Server for TravelHax0r flight search functionality.
Provides a single tool to search for flights using the fast_flights library.
"""

from enum import StrEnum

from fastmcp import FastMCP

from fast_flights import FlightData, Passengers, TFSData, aget_flights_from_filter

from .utils import parse_duration, parse_price


class SortBy(StrEnum):
    PRICE = "price"
    DURATION = "duration"
    STOPS = "stops"


class TripType(StrEnum):
    ROUND_TRIP = "round-trip"
    ONE_WAY = "one-way"


class Seat(StrEnum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium-economy"
    BUSINESS = "business"
    FIRST = "first"


# Create the MCP server
app = FastMCP("travelhax0r")


@app.tool()
async def search_flights(
    departure_date: str,
    from_airport: str,
    to_airport: str,
    return_date: str | None = None,
    trip_type: TripType = TripType.ROUND_TRIP,
    seat: Seat = Seat.ECONOMY,
    adults: int = 1,
    children: int = 0,
    infants_in_seat: int = 0,
    infants_on_lap: int = 0,
    currency: str = "USD",
    sort_by: SortBy = SortBy.PRICE,
) -> str:
    """
    Search for flights using the fast_flights library.

    Args:
        departure_date: Departure date in YYYY-MM-DD format
        from_airport: Departure airport code (e.g., "BER")
        to_airport: Arrival airport code (e.g., "MCO")
        return_date: Return date in YYYY-MM-DD format (required for round-trip)
        trip_type: Type of trip - "round-trip" or "one-way"
        seat: Seat class - "economy", "premium-economy", "business", or "first"
        adults: Number of adult passengers
        children: Number of child passengers
        infants_in_seat: Number of infants in seats
        infants_on_lap: Number of infants on lap
        currency: Currency code for prices (e.g., "USD")
        sort_by: How to sort results - "price", "duration", or "stops" (default: "price")

    Returns:
        Formatted string with flight search results
    """
    try:
        # Create passengers object
        passengers = Passengers(
            adults=adults,
            children=children,
            infants_in_seat=infants_in_seat,
            infants_on_lap=infants_on_lap,
        )

        # Create flight data based on trip type
        flight_data = []

        if trip_type == "round-trip":
            if not return_date:
                raise ValueError("return_date is required for round-trip flights")
            flight_data = [
                FlightData(
                    date=departure_date,
                    from_airport=from_airport,
                    to_airport=to_airport,
                ),
                FlightData(
                    date=return_date, from_airport=to_airport, to_airport=from_airport
                ),
            ]
        elif trip_type == "one-way":
            flight_data = [
                FlightData(
                    date=departure_date,
                    from_airport=from_airport,
                    to_airport=to_airport,
                ),
            ]

        # Create TFS data
        tfs_data = TFSData.from_interface(
            flight_data=flight_data,
            trip=trip_type,
            seat=seat,
            passengers=passengers,
        )

        # Search for flights
        result = await aget_flights_from_filter(
            tfs_data,
            mode="local",
            currency=currency,
        )

        if result is None:
            return "No flights found for the given search criteria."

        # Sort flights based on sort_by parameter
        if sort_by == SortBy.PRICE:
            result.flights.sort(key=lambda f: parse_price(f.price))
        elif sort_by == SortBy.DURATION:
            result.flights.sort(key=lambda f: parse_duration(f.duration))
        elif sort_by == SortBy.STOPS:
            result.flights.sort(
                key=lambda f: f.stops if isinstance(f.stops, int) else 999
            )

        # Format the results
        output = []
        output.append(f"Current price range: {result.current_price}")
        output.append(f"Found {len(result.flights)} flights\n")

        for i, flight in enumerate(result.flights[:10]):  # Show first 10 flights
            best_marker = " ⭐ BEST" if flight.is_best else ""
            output.append(f"Flight {i+1}:{best_marker}")
            output.append(f"  Airline: {flight.name}")
            output.append(f"  Departure: {flight.departure}")
            output.append(f"  Arrival: {flight.arrival}")
            if flight.arrival_time_ahead:
                output.append(f"  Time ahead: {flight.arrival_time_ahead}")
            output.append(f"  Duration: {flight.duration}")
            output.append(f"  Stops: {flight.stops}")
            if flight.delay:
                output.append(f"  Delay: {flight.delay}")
            output.append(f"  Price: {flight.price}")
            output.append("")

        if len(result.flights) > 10:
            output.append(f"... and {len(result.flights) - 10} more flights")

        return "\n".join(output)

    except Exception as e:
        return f"Error searching for flights: {e!s}"


if __name__ == "__main__":
    app.run()
