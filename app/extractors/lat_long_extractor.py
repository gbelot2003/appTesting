# File path: app/extractors/lat_long_extractor.py

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

class LatLongExtractor:
    def __init__(self, user_agent="address_locator"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def obtener_lat_long(self, address):
        """
        Extrae la latitud y longitud de una dirección usando geopy.
        :param address: Dirección completa como cadena.
        :return: (latitud, longitud) como una tupla o None si no se encuentra.
        """
        try:
            location = self.geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
        except GeopyError as e:
            print(f"Error al intentar obtener las coordenadas: {e}")
        return None, None
