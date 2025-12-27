import openmeteo_requests
from .geo import get_coordinates
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def temperature(lat,long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": lat ,
	    "longitude": long,
	    "hourly": "temperature_2m",
	    "current": ["rain", "apparent_temperature"],
    }
    responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_rain = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()

    print(f"\nCurrent time: {current.Time()}")
    print(f"Current rain: {current_rain}")
    print(f"Current apparent_temperature: {current_apparent_temperature}")

# Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
	    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	    end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
#last_hour = hourly_dataframe.iloc[[-1]]
    print("\nHourly data\n",hourly_dataframe)
    return hourly_dataframe







































