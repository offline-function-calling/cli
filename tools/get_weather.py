import requests


class WeatherError(Exception):
    pass


def get_weather(location: str):
    """
    Fetches the current weather conditions for a specified location at the present time.

    For the model: Use this tool whenever the user asks about the weather. You
    must extract a location (city name, zip code, airport code, landmark, etc.)
    from the user's prompt to use as the 'location' parameter.

    Args:
        location (str): The city or location to get the weather for (e.g., "Paris").

    Returns:
        dict: A dictionary containing detailed weather data from wttr.in.

    Raises:
        WeatherError: If the weather data cannot be fetched, or the location is
                      invalid.
    """
    try:
        url = f"https://wttr.in/{location}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        data = data["current_condition"][0]
        return {
            "units": "metric",
            "condition": data["weatherDesc"][0]["value"],
            "temperature": int(data["temp_C"]),
            "feels_like": int(data["FeelsLikeC"]),
            "wind_speed": int(data["windspeedKmph"]),
        }
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"Could not fetch weather data for '{location}': {e}")
