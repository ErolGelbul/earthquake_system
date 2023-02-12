from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")
city = "Mersin"

location = geolocator.geocode(city)
print("Latitude:", location.latitude)
print("Longitude:", location.longitude)


def get_location(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude
