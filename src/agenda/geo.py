from geopy.geocoders import Nominatim

# Optional: Bypassing SSL verification for some environments
# context = ssl.create_default_context()
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE

def get_lat_long(city_name):
    """
    Converts a city name to latitude and longitude coordinates.
    
    Args:
        city_name (str): The name of the city (e.g., "Paris, France").
        
    Returns:
        tuple: A tuple containing (latitude, longitude) or None if not found.
    """
    # Initialize Nominatim API with a custom user_agent
    # It is important to specify a unique user agent
    try:
        geolocator = Nominatim(user_agent="city_converter_app", timeout=10)
        
        # Geocode the city name
        location = geolocator.geocode(city_name)
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
def get_coordinates(city):
    coordinates = get_lat_long(city)

    if coordinates:
        latitude, longitude = coordinates
        return latitude, longitude
    
    else:
        print(f"Could not find coordinates for {city}")



