# Project Requirements Document (PRD)

## 1. Project Summary

The main objective of this project is to develop a Python backend that extracts the average price of commercial properties located near bus stops in Valladolid, Spain.

-   **Location source:** Google Maps API, which allows obtaining bus stop coordinates.
-   **Price data source:** Idealista API. However, for this first version, the `idealista_data.csv` file with pre-existing data will be used directly.
-   **Output:** A CSV file showing, for each bus stop, the average price of commercial properties at different distances.

## 2. Objectives

-   **2.1 Geographic data extraction:**  
    Connect to the Google Maps API to obtain the location (latitude and longitude) of bus stops in a given area.

-   **2.2 Commercial data processing:**  
    Analyze and process the information contained in `idealista_data.csv` to obtain prices and other property details.

-   **2.3 Average price calculation:**  
    Calculate the average price of properties near each stop, considering different distance ranges.

-   **2.4 CSV output generation:**  
    Consolidate results and export them to a CSV file for subsequent analysis or visualization.

## 3. Project Scope

-   **Main functionalities:**

    -   Obtaining bus stops using the Google Maps API.
    -   Analysis and processing of commercial property data from `idealista_data.csv`.
    -   Calculation of average prices based on proximity to each bus stop.
    -   Generation of a CSV file with results.

-   **Current limitations:**
    -   The Idealista API will not be used in this version; instead, we will work directly with pre-existing data in the CSV.
-   **Possible future improvements:**
    -   Integrate the Idealista API to obtain real-time data.
    -   Modularize and refactor the system as new functionalities are added, maintaining project scalability.

## 4. Functional Requirements

### 4.1. Bus Stop Extraction

-   Connect to Google Maps API using the API key stored in the `.env` file.
-   Search for bus stops near a specific location (latitude and longitude).
-   Extract and store coordinates (latitude and longitude) of each stop found.

_Review the following code example to understand the logic to implement:_

```python
import os
import googlemaps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Maps client
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)

def get_bus_stations(location): # Search for bus stations near the given location
    places_result = gmaps.places_nearby(location=location, radius=5000, type='bus_station')
    # Extract coordinates of each bus station
    bus_stations = []
    for place in places_result.get('results', []):
        lat = place['geometry']['location']['lat']
        lng = place['geometry']['location']['lng']
        bus_stations.append((lat, lng))
    return bus_stations

def main(): # Example input: latitude and longitude
    location = (40.416775, -3.703790) # Madrid, Spain
    bus_stations = get_bus_stations(location)
    print("Bus Stations Coordinates:", bus_stations)

if __name__ == "__main__":
    main()
```

### 4.2. Idealista Data Processing

-   Read and analyze the `idealista_data.csv` file to extract basic information for each property: price, size, location (latitude and longitude), among others.
-   Identify and filter properties based on distance to each bus stop.
-   Calculate the average price of properties within predefined distance intervals.

_Below is an example of the CSV data file content:_

```csv
floor,price,size,exterior,rooms,bathrooms,latitude,longitude,showAddress,url,distance,priceByArea
7,360000.0,138.0,True,3,2,41.6494433,-4.7200854,True,https://www.idealista.com/inmueble/106392059/,617,2609.0
4,297000.0,111.0,True,2,2,41.6512257,-4.7246405,True,https://www.idealista.com/inmueble/104934785/,425,2676.0
4,110000.0,81.0,True,3,1,41.6459407,-4.7147159,False,https://www.idealista.com/inmueble/106328678/,1169,1358.0
4,114500.0,69.0,True,2,1,41.6589796,-4.7240359,False,https://www.idealista.com/inmueble/106739392/,492,1659.0
1,293000.0,122.0,True,3,2,41.6452487,-4.7239924,False,https://www.idealista.com/inmueble/106684482/,1058,2402.0
1,144900.0,111.0,True,3,2,41.6385242,-4.7254651,False,https://www.idealista.com/inmueble/106437770/,1815,1305.0
4,79000.0,59.0,True,3,1,41.6469732,-4.7105617,False,https://www.idealista.com/inmueble/106544239/,1312,1339.0
```

### 4.3. Output File Generation

-   Consolidate processed results in a structured CSV file.
-   Each CSV record should include:
    -   Bus stop location.
    -   For each distance range (e.g., within 500m, 1000m, etc.), the calculated average property price.
-   The CSV structure should facilitate subsequent analysis or import into visualization tools.

## 5. Technical Requirements

-   **Language:** Python 3.10.
-   **Dependencies:**
    -   `googlemaps` for connecting and querying the Google Maps API.
    -   `python-dotenv` for loading environment variables.
    -   `pandas` (optional, but recommended) for CSV file processing.
-   **Security and Configuration:**  
    API keys and sensitive data must be stored in the `.env` file and not included directly in the source code.

## 6. Project File Structure

Given the requirement to minimize the number of files, the following structure is proposed:

```plaintext
idealista-property-search/
├── main.py              # Main script containing all logic:
│                        # - Configuration loading from .env
│                        # - Bus stop retrieval via Google Maps API
│                        # - Reading and processing `idealista_data.csv`
│                        # - Calculation and export of CSV with price averages
├── idealista_data.csv   # Data file with commercial property information
├── .env                 # Configuration file for sensitive variables (e.g., API Keys)
└── instructions.md      # Detailed project documentation and guidelines
```

## 7. Additional Considerations and Recommendations

-   **Modularity and Scalability:**  
    Although the initial implementation will be concentrated in a single file (`main.py`), it is recommended to refactor and divide the code into modules in future versions to improve maintainability and facilitate unit testing.

-   **Error Handling:**  
    Implement a robust mechanism for error handling, especially in connecting to external services (Google Maps API) and during CSV data processing.

-   **Testing and Validation:**  
    Include unit and integration tests to validate that each component (location extraction, CSV processing, average calculation, and CSV output generation) works in isolation and together.

-   **Code Documentation:**  
    Code comments should be in English for consistency, while general project documentation and this PRD remain in Spanish.

## 8. Complementary Documentation

Developers are recommended to consult the following examples included in the project documentation for better understanding:

-   **Bus stop extraction example (Google Maps API):**  
    See the section in `instructions.md` showing the use of the Google Maps API to obtain nearby bus stops.

-   **Data format example in `idealista_data.csv`:**  
    The provided CSV data sample illustrates the type of information to work with and the fields to be considered during processing.

This document establishes the essential guidelines and necessary context for developing the desired functionality. Developers are recommended to use this PRD as a reference during project implementation to ensure compliance with all requirements and proper integration of system components.
