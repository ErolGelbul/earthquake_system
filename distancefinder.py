
# Find the distance between two points using Haversine formula

def haversine(city):
    import math
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    lat1, lon1 = location.latitude, location.longitude

    lat2 = 36.7978381
    lon2 = 34.6298391
    R = 6371  # Radius of the earth in km
    dLat = math.radians(lat2 - lat1)  # Convert to radians
    dLon = math.radians(lon2 - lon1)  # Convert to radians
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # Distance in km
    return d
