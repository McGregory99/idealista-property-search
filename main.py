import os
from typing import List, Tuple, Dict, Optional
import googlemaps
from dotenv import load_dotenv
from dataclasses import dataclass
from time import sleep
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

@dataclass
class BusStation:
    """Represents a bus station with its location and metadata"""
    latitude: float
    longitude: float
    name: str
    place_id: str
    formatted_address: Optional[str] = None
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    formatted_phone_number: Optional[str] = None
    opening_hours: Optional[List[str]] = None

@dataclass
class Property:
    """Represents a commercial property with its details"""
    latitude: float
    longitude: float
    price: float
    size: float
    floor: str
    rooms: Optional[int]
    bathrooms: Optional[int]
    price_per_area: float
    url: str
    
class BusStationExtractor:
    """Handles the extraction of bus station data from Google Maps API"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key and initialize Google Maps client
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in .env file")
            
        self.gmaps = googlemaps.Client(key=api_key)
        
    def get_place_details(self, place_id: str) -> Dict:
        """
        Get detailed information about a specific place
        
        Args:
            place_id: The Google Places ID of the location
            
        Returns:
            Dictionary with place details
        """
        try:
            result = self.gmaps.place(
                place_id,
                fields=['name', 'formatted_address', 'rating', 
                       'user_ratings_total', 'formatted_phone_number',
                       'opening_hours']
            )
            return result.get('result', {})
        except Exception as e:
            print(f"Error fetching place details for {place_id}: {str(e)}")
            return {}
    
    def create_bus_station(self, place: Dict) -> BusStation:
        """
        Create a BusStation object from place data
        
        Args:
            place: Dictionary containing place information
            
        Returns:
            BusStation object
        """
        location = place['geometry']['location']
        place_id = place['place_id']
        
        # Get additional details
        details = self.get_place_details(place_id)
        
        return BusStation(
            latitude=location['lat'],
            longitude=location['lng'],
            name=place.get('name', 'Unknown'),
            place_id=place_id,
            formatted_address=details.get('formatted_address'),
            rating=details.get('rating'),
            user_ratings_total=details.get('user_ratings_total'),
            formatted_phone_number=details.get('formatted_phone_number'),
            opening_hours=details.get('opening_hours', {}).get('weekday_text')
        )
    
    def get_bus_stations(self, 
                        center: Tuple[float, float], 
                        radius: int = 5000) -> List[BusStation]:
        """
        Retrieve bus stations within a specified radius from a center point
        
        Args:
            center: Tuple of (latitude, longitude)
            radius: Search radius in meters (max 50000)
            
        Returns:
            List of BusStation objects
        """
        bus_stations = []
        next_page_token = None
        
        try:
            while True:
                # Make API request
                results = self.gmaps.places_nearby(
                    location=center,
                    radius=radius,
                    type='bus_station',
                    page_token=next_page_token
                )
                
                # Process results
                for place in results.get('results', []):
                    bus_station = self.create_bus_station(place)
                    bus_stations.append(bus_station)
                
                # Check for next page
                next_page_token = results.get('next_page_token')
                if not next_page_token:
                    break
                    
                # Wait before making next request (API requirement)
                sleep(2)
                
        except Exception as e:
            print(f"Error fetching bus stations: {str(e)}")
            raise
            
        return bus_stations

class PropertyDataProcessor:
    """Handles the processing of property data from CSV"""
    
    def __init__(self, csv_path: str = 'idealista_data.csv'):
        """
        Initialize the processor with the CSV file path
        
        Args:
            csv_path: Path to the CSV file containing property data
        """
        try:
            self.df = pd.read_csv(csv_path)
            self._validate_data()
            self.properties = self._load_properties()
        except Exception as e:
            print(f"Error loading property data: {str(e)}")
            raise
    
    def _validate_data(self):
        """Validate that the CSV has all required columns"""
        required_columns = [
            'latitude', 'longitude', 'price', 'size', 'floor',
            'rooms', 'bathrooms', 'priceByArea', 'url'
        ]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _load_properties(self) -> List[Property]:
        """Convert DataFrame rows to Property objects"""
        properties = []
        for _, row in self.df.iterrows():
            try:
                # Handle potential NaN values for rooms and bathrooms
                rooms = int(row['rooms']) if pd.notna(row['rooms']) else None
                bathrooms = int(row['bathrooms']) if pd.notna(row['bathrooms']) else None
                
                property = Property(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    price=float(row['price']),
                    size=float(row['size']),
                    floor=str(row['floor']).lower(),
                    rooms=rooms,
                    bathrooms=bathrooms,
                    price_per_area=float(row['priceByArea']),
                    url=str(row['url'])
                )
                properties.append(property)
            except Exception as e:
                print(f"Error processing property row {_}: {str(e)}")
                continue
        
        if not properties:
            raise ValueError("No properties could be loaded from the CSV file")
            
        return properties
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the distance between two points using the Haversine formula
        
        Args:
            lat1, lon1: Coordinates of first point
            lat2, lon2: Coordinates of second point
            
        Returns:
            Distance in meters
        """
        R = 6371000  # Earth's radius in meters
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def get_properties_near_station(self, 
                                  station: BusStation, 
                                  max_distance: float) -> List[Property]:
        """
        Get properties within a specified distance from a bus station
        
        Args:
            station: BusStation object
            max_distance: Maximum distance in meters
            
        Returns:
            List of Property objects within the specified distance
        """
        nearby_properties = []
        
        for property in self.properties:
            distance = self.calculate_distance(
                station.latitude, station.longitude,
                property.latitude, property.longitude
            )
            
            if distance <= max_distance:
                nearby_properties.append(property)
                
        return nearby_properties
    
    def calculate_average_price_by_distance(self, 
                                          station: BusStation,
                                          distance_ranges: List[int]) -> Dict[int, Dict]:
        """
        Calculate average property prices and counts for different distance ranges
        
        Args:
            station: BusStation object
            distance_ranges: List of distances in meters to check
            
        Returns:
            Dictionary with distance as key and stats as value
        """
        stats = {}
        
        for distance in distance_ranges:
            properties = self.get_properties_near_station(station, distance)
            if properties:
                avg_price = sum(p.price for p in properties) / len(properties)
                avg_price_per_m2 = sum(p.price_per_area for p in properties) / len(properties)
                stats[distance] = {
                    'avg_price': avg_price,
                    'avg_price_per_m2': avg_price_per_m2,
                    'property_count': len(properties)
                }
            else:
                stats[distance] = {
                    'avg_price': 0,
                    'avg_price_per_m2': 0,
                    'property_count': 0
                }
                
        return stats

def main():
    # Coordinates for Valladolid city center
    VALLADOLID_CENTER = (41.652251, -4.724532)
    DISTANCE_RANGES = [500, 1000, 2000]  # meters
    
    try:
        # Initialize extractor and processor
        extractor = BusStationExtractor()
        processor = PropertyDataProcessor()
        
        # Get bus stations
        bus_stations = extractor.get_bus_stations(
            center=VALLADOLID_CENTER,
            radius=10000
        )
        
        # Process and print results
        print(f"\nAnalyzing {len(bus_stations)} bus stations:")
        for station in bus_stations:
            print(f"\n{station.name}")
            print(f"Location: ({station.latitude}, {station.longitude})")
            
            # Calculate statistics for different distances
            stats = processor.calculate_average_price_by_distance(
                station, DISTANCE_RANGES
            )
            
            # Print statistics
            for distance, data in stats.items():
                if data['property_count'] > 0:
                    print(f"\nProperties within {distance}m:")
                    print(f"  Count: {data['property_count']}")
                    print(f"  Average price: €{data['avg_price']:,.2f}")
                    print(f"  Average price/m²: €{data['avg_price_per_m2']:,.2f}")
            print("-" * 50)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 