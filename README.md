# Commercial Property Price Analysis near Bus Stops

This project develops an application that analyzes and calculates the average price of commercial properties located near bus stops in Valladolid, Spain.

## 🎯 Description

The system processes bus stop location data using the Google Maps API and combines it with commercial property information to generate price analyses by proximity.

## ⚙️ System Requirements

-   Python 3.10 or higher
-   Internet connection (for Google Maps API)
-   Data file `idealista_data.csv`

### Main Dependencies

-   `googlemaps`: To interact with the Google Maps API
-   `python-dotenv`: For environment variable management
-   `pandas`: For CSV data processing

## 🚀 Installation

1. Clone the repository:

```bash
git clone [REPOSITORY_URL]
cd [DIRECTORY_NAME]
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
    - Create a `.env` file in the project root
    - Add your Google Maps API key:
        ```
        GOOGLE_MAPS_API_KEY=your_api_key_here
        ```

## 📁 Project Structure

```
project_root/
├── main.py              # Main script
├── idealista_data.csv   # Property data
├── .env                 # Environment variables
└── README.md            # Documentation
```

## 💻 Usage

1. Ensure you have the `idealista_data.csv` file in the project directory
2. Run the main script:

```bash
python main.py
```

## 📊 Data Format

### Input (idealista_data.csv)

The input CSV file must contain the following fields:

-   floor: Property floor
-   price: Price in euros
-   size: Size in square meters
-   exterior: Boolean (True/False)
-   rooms: Number of rooms
-   bathrooms: Number of bathrooms
-   latitude: Latitude
-   longitude: Longitude
-   showAddress: Boolean (True/False)
-   url: Property URL
-   distance: Distance in meters
-   priceByArea: Price per square meter

### Output

A CSV file will be generated with:

-   Bus stop location
-   Average prices by distance ranges

## 🔒 Security

-   Do not share your `.env` file or expose API keys
-   Keep your Python version and dependencies up to date

## 🤝 Contributions

Contributions are welcome. Please ensure to:

1. Fork the repository
2. Create a branch for your feature
3. Follow existing code conventions
4. Document your changes
5. Submit a Pull Request

## 📝 Additional Notes

-   This project is in its first version and uses pre-existing CSV data
-   Future versions may include direct integration with the Idealista API
-   It is recommended to consult the full documentation in `instructions.md`
