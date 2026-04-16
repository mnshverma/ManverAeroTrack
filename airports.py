"""
ManwarAeroTrack - Airport Database
Comprehensive IATA airport lookup with coordinates for weather and routing.
"""

AIRPORTS = {
    # India
    "DEL": {"name": "Indira Gandhi International Airport", "city": "New Delhi", "country": "India", "lat": 28.5665, "lon": 77.1031, "tz": "Asia/Kolkata"},
    "BOM": {"name": "Chhatrapati Shivaji Maharaj International Airport", "city": "Mumbai", "country": "India", "lat": 19.0896, "lon": 72.8656, "tz": "Asia/Kolkata"},
    "BLR": {"name": "Kempegowda International Airport", "city": "Bengaluru", "country": "India", "lat": 13.1979, "lon": 77.7063, "tz": "Asia/Kolkata"},
    "MAA": {"name": "Chennai International Airport", "city": "Chennai", "country": "India", "lat": 12.9900, "lon": 80.1693, "tz": "Asia/Kolkata"},
    "CCU": {"name": "Netaji Subhas Chandra Bose International Airport", "city": "Kolkata", "country": "India", "lat": 22.6549, "lon": 88.4467, "tz": "Asia/Kolkata"},
    "HYD": {"name": "Rajiv Gandhi International Airport", "city": "Hyderabad", "country": "India", "lat": 17.2403, "lon": 78.4294, "tz": "Asia/Kolkata"},
    "COK": {"name": "Cochin International Airport", "city": "Kochi", "country": "India", "lat": 10.1520, "lon": 76.4019, "tz": "Asia/Kolkata"},
    "AMD": {"name": "Sardar Vallabhbhai Patel International Airport", "city": "Ahmedabad", "country": "India", "lat": 23.0771, "lon": 72.6347, "tz": "Asia/Kolkata"},
    "PNQ": {"name": "Pune Airport", "city": "Pune", "country": "India", "lat": 18.5822, "lon": 73.9197, "tz": "Asia/Kolkata"},
    "JAI": {"name": "Jaipur International Airport", "city": "Jaipur", "country": "India", "lat": 26.8242, "lon": 75.8122, "tz": "Asia/Kolkata"},
    "GOI": {"name": "Dabolim Airport", "city": "Goa", "country": "India", "lat": 15.3808, "lon": 73.8314, "tz": "Asia/Kolkata"},
    "IXC": {"name": "Chandigarh International Airport", "city": "Chandigarh", "country": "India", "lat": 30.6735, "lon": 76.7885, "tz": "Asia/Kolkata"},
    "IXB": {"name": "Bagdogra Airport", "city": "Siliguri", "country": "India", "lat": 26.6812, "lon": 88.3286, "tz": "Asia/Kolkata"},
    "LKO": {"name": "Chaudhary Charan Singh International Airport", "city": "Lucknow", "country": "India", "lat": 26.7606, "lon": 80.8893, "tz": "Asia/Kolkata"},
    "VNS": {"name": "Lal Bahadur Shastri International Airport", "city": "Varanasi", "country": "India", "lat": 25.4524, "lon": 82.8593, "tz": "Asia/Kolkata"},
    "PAT": {"name": "Jay Prakash Narayan Airport", "city": "Patna", "country": "India", "lat": 25.5913, "lon": 85.0880, "tz": "Asia/Kolkata"},
    "SXR": {"name": "Sheikh ul Alam Airport", "city": "Srinagar", "country": "India", "lat": 33.9871, "lon": 74.7742, "tz": "Asia/Kolkata"},
    "TRV": {"name": "Trivandrum International Airport", "city": "Thiruvananthapuram", "country": "India", "lat": 8.4821, "lon": 76.9201, "tz": "Asia/Kolkata"},
    "IXM": {"name": "Madurai Airport", "city": "Madurai", "country": "India", "lat": 9.8345, "lon": 78.0934, "tz": "Asia/Kolkata"},
    "NAG": {"name": "Dr. Babasaheb Ambedkar International Airport", "city": "Nagpur", "country": "India", "lat": 21.0922, "lon": 79.0472, "tz": "Asia/Kolkata"},

    # Middle East
    "DXB": {"name": "Dubai International Airport", "city": "Dubai", "country": "UAE", "lat": 25.2532, "lon": 55.3657, "tz": "Asia/Dubai"},
    "AUH": {"name": "Abu Dhabi International Airport", "city": "Abu Dhabi", "country": "UAE", "lat": 24.4330, "lon": 54.6511, "tz": "Asia/Dubai"},
    "DOH": {"name": "Hamad International Airport", "city": "Doha", "country": "Qatar", "lat": 25.2731, "lon": 51.6080, "tz": "Asia/Qatar"},
    "BAH": {"name": "Bahrain International Airport", "city": "Manama", "country": "Bahrain", "lat": 26.2708, "lon": 50.6336, "tz": "Asia/Bahrain"},
    "KWI": {"name": "Kuwait International Airport", "city": "Kuwait City", "country": "Kuwait", "lat": 29.2267, "lon": 47.9689, "tz": "Asia/Kuwait"},
    "MCT": {"name": "Muscat International Airport", "city": "Muscat", "country": "Oman", "lat": 23.5933, "lon": 58.2844, "tz": "Asia/Muscat"},
    "RUH": {"name": "King Khalid International Airport", "city": "Riyadh", "country": "Saudi Arabia", "lat": 24.9578, "lon": 46.6989, "tz": "Asia/Riyadh"},
    "JED": {"name": "King Abdulaziz International Airport", "city": "Jeddah", "country": "Saudi Arabia", "lat": 21.6796, "lon": 39.1565, "tz": "Asia/Riyadh"},

    # Europe
    "LHR": {"name": "London Heathrow Airport", "city": "London", "country": "UK", "lat": 51.4700, "lon": -0.4543, "tz": "Europe/London"},
    "LGW": {"name": "London Gatwick Airport", "city": "London", "country": "UK", "lat": 51.1537, "lon": -0.1821, "tz": "Europe/London"},
    "CDG": {"name": "Charles de Gaulle Airport", "city": "Paris", "country": "France", "lat": 49.0097, "lon": 2.5479, "tz": "Europe/Paris"},
    "AMS": {"name": "Amsterdam Airport Schiphol", "city": "Amsterdam", "country": "Netherlands", "lat": 52.3105, "lon": 4.7683, "tz": "Europe/Amsterdam"},
    "FRA": {"name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "lat": 50.0379, "lon": 8.5622, "tz": "Europe/Berlin"},
    "MUC": {"name": "Munich Airport", "city": "Munich", "country": "Germany", "lat": 48.3537, "lon": 11.7750, "tz": "Europe/Berlin"},
    "ZRH": {"name": "Zurich Airport", "city": "Zurich", "country": "Switzerland", "lat": 47.4647, "lon": 8.5492, "tz": "Europe/Zurich"},
    "MAD": {"name": "Adolfo Suárez Madrid–Barajas Airport", "city": "Madrid", "country": "Spain", "lat": 40.4719, "lon": -3.5626, "tz": "Europe/Madrid"},
    "BCN": {"name": "Josep Tarradellas Barcelona–El Prat Airport", "city": "Barcelona", "country": "Spain", "lat": 41.2971, "lon": 2.0785, "tz": "Europe/Madrid"},
    "FCO": {"name": "Leonardo da Vinci–Fiumicino Airport", "city": "Rome", "country": "Italy", "lat": 41.8003, "lon": 12.2389, "tz": "Europe/Rome"},
    "MXP": {"name": "Milan Malpensa Airport", "city": "Milan", "country": "Italy", "lat": 45.6306, "lon": 8.7281, "tz": "Europe/Rome"},
    "CPH": {"name": "Copenhagen Airport", "city": "Copenhagen", "country": "Denmark", "lat": 55.6181, "lon": 12.6560, "tz": "Europe/Copenhagen"},
    "ARN": {"name": "Stockholm Arlanda Airport", "city": "Stockholm", "country": "Sweden", "lat": 59.6519, "lon": 17.9186, "tz": "Europe/Stockholm"},
    "OSL": {"name": "Oslo Gardermoen Airport", "city": "Oslo", "country": "Norway", "lat": 60.1939, "lon": 11.1004, "tz": "Europe/Oslo"},
    "HEL": {"name": "Helsinki-Vantaa Airport", "city": "Helsinki", "country": "Finland", "lat": 60.3172, "lon": 24.9633, "tz": "Europe/Helsinki"},
    "VIE": {"name": "Vienna International Airport", "city": "Vienna", "country": "Austria", "lat": 48.1102, "lon": 16.5697, "tz": "Europe/Vienna"},
    "BRU": {"name": "Brussels Airport", "city": "Brussels", "country": "Belgium", "lat": 50.9014, "lon": 4.4844, "tz": "Europe/Brussels"},
    "IST": {"name": "Istanbul Airport", "city": "Istanbul", "country": "Turkey", "lat": 41.2608, "lon": 28.7418, "tz": "Europe/Istanbul"},
    "ATH": {"name": "Athens International Airport", "city": "Athens", "country": "Greece", "lat": 37.9364, "lon": 23.9445, "tz": "Europe/Athens"},
    "WAW": {"name": "Warsaw Chopin Airport", "city": "Warsaw", "country": "Poland", "lat": 52.1657, "lon": 20.9671, "tz": "Europe/Warsaw"},
    "PRG": {"name": "Václav Havel Airport Prague", "city": "Prague", "country": "Czech Republic", "lat": 50.1008, "lon": 14.2600, "tz": "Europe/Prague"},
    "BUD": {"name": "Budapest Ferenc Liszt International Airport", "city": "Budapest", "country": "Hungary", "lat": 47.4298, "lon": 19.2611, "tz": "Europe/Budapest"},

    # Asia Pacific
    "SIN": {"name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915, "tz": "Asia/Singapore"},
    "KUL": {"name": "Kuala Lumpur International Airport", "city": "Kuala Lumpur", "country": "Malaysia", "lat": 2.7456, "lon": 101.7099, "tz": "Asia/Kuala_Lumpur"},
    "BKK": {"name": "Suvarnabhumi Airport", "city": "Bangkok", "country": "Thailand", "lat": 13.6900, "lon": 100.7501, "tz": "Asia/Bangkok"},
    "CGK": {"name": "Soekarno–Hatta International Airport", "city": "Jakarta", "country": "Indonesia", "lat": -6.1256, "lon": 106.6558, "tz": "Asia/Jakarta"},
    "MNL": {"name": "Ninoy Aquino International Airport", "city": "Manila", "country": "Philippines", "lat": 14.5086, "lon": 121.0197, "tz": "Asia/Manila"},
    "HKG": {"name": "Hong Kong International Airport", "city": "Hong Kong", "country": "China", "lat": 22.3080, "lon": 113.9185, "tz": "Asia/Hong_Kong"},
    "PEK": {"name": "Beijing Capital International Airport", "city": "Beijing", "country": "China", "lat": 40.0799, "lon": 116.6031, "tz": "Asia/Shanghai"},
    "PVG": {"name": "Shanghai Pudong International Airport", "city": "Shanghai", "country": "China", "lat": 31.1443, "lon": 121.8083, "tz": "Asia/Shanghai"},
    "CAN": {"name": "Guangzhou Baiyun International Airport", "city": "Guangzhou", "country": "China", "lat": 23.3924, "lon": 113.2988, "tz": "Asia/Shanghai"},
    "NRT": {"name": "Narita International Airport", "city": "Tokyo", "country": "Japan", "lat": 35.7720, "lon": 140.3929, "tz": "Asia/Tokyo"},
    "HND": {"name": "Haneda Airport", "city": "Tokyo", "country": "Japan", "lat": 35.5494, "lon": 139.7798, "tz": "Asia/Tokyo"},
    "KIX": {"name": "Kansai International Airport", "city": "Osaka", "country": "Japan", "lat": 34.4272, "lon": 135.2440, "tz": "Asia/Tokyo"},
    "ICN": {"name": "Incheon International Airport", "city": "Seoul", "country": "South Korea", "lat": 37.4602, "lon": 126.4407, "tz": "Asia/Seoul"},
    "TPE": {"name": "Taiwan Taoyuan International Airport", "city": "Taipei", "country": "Taiwan", "lat": 25.0777, "lon": 121.2328, "tz": "Asia/Taipei"},
    "SYD": {"name": "Sydney Kingsford Smith Airport", "city": "Sydney", "country": "Australia", "lat": -33.9399, "lon": 151.1753, "tz": "Australia/Sydney"},
    "MEL": {"name": "Melbourne Airport", "city": "Melbourne", "country": "Australia", "lat": -37.6690, "lon": 144.8410, "tz": "Australia/Melbourne"},
    "BNE": {"name": "Brisbane Airport", "city": "Brisbane", "country": "Australia", "lat": -27.3842, "lon": 153.1175, "tz": "Australia/Brisbane"},
    "PER": {"name": "Perth Airport", "city": "Perth", "country": "Australia", "lat": -31.9403, "lon": 115.9669, "tz": "Australia/Perth"},
    "AKL": {"name": "Auckland Airport", "city": "Auckland", "country": "New Zealand", "lat": -37.0082, "lon": 174.7850, "tz": "Pacific/Auckland"},
    "CMB": {"name": "Bandaranaike International Airport", "city": "Colombo", "country": "Sri Lanka", "lat": 7.1808, "lon": 79.8841, "tz": "Asia/Colombo"},
    "DAC": {"name": "Hazrat Shahjalal International Airport", "city": "Dhaka", "country": "Bangladesh", "lat": 23.8433, "lon": 90.3978, "tz": "Asia/Dhaka"},
    "KTM": {"name": "Tribhuvan International Airport", "city": "Kathmandu", "country": "Nepal", "lat": 27.6966, "lon": 85.3591, "tz": "Asia/Kathmandu"},

    # Americas
    "JFK": {"name": "John F. Kennedy International Airport", "city": "New York", "country": "USA", "lat": 40.6413, "lon": -73.7781, "tz": "America/New_York"},
    "EWR": {"name": "Newark Liberty International Airport", "city": "Newark", "country": "USA", "lat": 40.6895, "lon": -74.1745, "tz": "America/New_York"},
    "LAX": {"name": "Los Angeles International Airport", "city": "Los Angeles", "country": "USA", "lat": 33.9425, "lon": -118.4081, "tz": "America/Los_Angeles"},
    "SFO": {"name": "San Francisco International Airport", "city": "San Francisco", "country": "USA", "lat": 37.6213, "lon": -122.3790, "tz": "America/Los_Angeles"},
    "ORD": {"name": "O'Hare International Airport", "city": "Chicago", "country": "USA", "lat": 41.9742, "lon": -87.9073, "tz": "America/Chicago"},
    "MIA": {"name": "Miami International Airport", "city": "Miami", "country": "USA", "lat": 25.7959, "lon": -80.2870, "tz": "America/New_York"},
    "ATL": {"name": "Hartsfield–Jackson Atlanta International Airport", "city": "Atlanta", "country": "USA", "lat": 33.6407, "lon": -84.4277, "tz": "America/New_York"},
    "DFW": {"name": "Dallas/Fort Worth International Airport", "city": "Dallas", "country": "USA", "lat": 32.8998, "lon": -97.0403, "tz": "America/Chicago"},
    "SEA": {"name": "Seattle-Tacoma International Airport", "city": "Seattle", "country": "USA", "lat": 47.4502, "lon": -122.3088, "tz": "America/Los_Angeles"},
    "BOS": {"name": "Logan International Airport", "city": "Boston", "country": "USA", "lat": 42.3656, "lon": -71.0096, "tz": "America/New_York"},
    "IAD": {"name": "Washington Dulles International Airport", "city": "Washington D.C.", "country": "USA", "lat": 38.9531, "lon": -77.4565, "tz": "America/New_York"},
    "IAH": {"name": "George Bush Intercontinental Airport", "city": "Houston", "country": "USA", "lat": 29.9902, "lon": -95.3368, "tz": "America/Chicago"},
    "DEN": {"name": "Denver International Airport", "city": "Denver", "country": "USA", "lat": 39.8561, "lon": -104.6737, "tz": "America/Denver"},
    "YYZ": {"name": "Toronto Pearson International Airport", "city": "Toronto", "country": "Canada", "lat": 43.6777, "lon": -79.6248, "tz": "America/Toronto"},
    "YVR": {"name": "Vancouver International Airport", "city": "Vancouver", "country": "Canada", "lat": 49.1967, "lon": -123.1815, "tz": "America/Vancouver"},
    "YUL": {"name": "Montreal-Pierre Elliott Trudeau International Airport", "city": "Montreal", "country": "Canada", "lat": 45.4706, "lon": -73.7408, "tz": "America/Montreal"},
    "GRU": {"name": "São Paulo/Guarulhos International Airport", "city": "São Paulo", "country": "Brazil", "lat": -23.4356, "lon": -46.4731, "tz": "America/Sao_Paulo"},
    "EZE": {"name": "Ministro Pistarini International Airport", "city": "Buenos Aires", "country": "Argentina", "lat": -34.8222, "lon": -58.5358, "tz": "America/Argentina/Buenos_Aires"},
    "MEX": {"name": "Benito Juárez International Airport", "city": "Mexico City", "country": "Mexico", "lat": 19.4363, "lon": -99.0721, "tz": "America/Mexico_City"},
    "BOG": {"name": "El Dorado International Airport", "city": "Bogotá", "country": "Colombia", "lat": 4.7016, "lon": -74.1469, "tz": "America/Bogota"},
    "SCL": {"name": "Arturo Merino Benítez International Airport", "city": "Santiago", "country": "Chile", "lat": -33.3930, "lon": -70.7858, "tz": "America/Santiago"},
    "LIM": {"name": "Jorge Chávez International Airport", "city": "Lima", "country": "Peru", "lat": -12.0219, "lon": -77.1143, "tz": "America/Lima"},

    # Africa
    "JNB": {"name": "O. R. Tambo International Airport", "city": "Johannesburg", "country": "South Africa", "lat": -26.1367, "lon": 28.2411, "tz": "Africa/Johannesburg"},
    "CPT": {"name": "Cape Town International Airport", "city": "Cape Town", "country": "South Africa", "lat": -33.9648, "lon": 18.6017, "tz": "Africa/Johannesburg"},
    "CAI": {"name": "Cairo International Airport", "city": "Cairo", "country": "Egypt", "lat": 30.1219, "lon": 31.4056, "tz": "Africa/Cairo"},
    "NBO": {"name": "Jomo Kenyatta International Airport", "city": "Nairobi", "country": "Kenya", "lat": -1.3192, "lon": 36.9275, "tz": "Africa/Nairobi"},
    "LOS": {"name": "Murtala Muhammed International Airport", "city": "Lagos", "country": "Nigeria", "lat": 6.5774, "lon": 3.3212, "tz": "Africa/Lagos"},
    "ACC": {"name": "Kotoka International Airport", "city": "Accra", "country": "Ghana", "lat": 5.6052, "lon": -0.1668, "tz": "Africa/Accra"},
    "ADD": {"name": "Addis Ababa Bole International Airport", "city": "Addis Ababa", "country": "Ethiopia", "lat": 8.9779, "lon": 38.7993, "tz": "Africa/Addis_Ababa"},
    "CMN": {"name": "Mohammed V International Airport", "city": "Casablanca", "country": "Morocco", "lat": 33.3675, "lon": -7.5898, "tz": "Africa/Casablanca"},
}


def get_airport(iata_code: str) -> dict | None:
    """Return airport info by IATA code (case-insensitive)."""
    return AIRPORTS.get(iata_code.upper().strip())


def search_airports(query: str) -> list[dict]:
    """Search airports by city, name, or IATA code."""
    query = query.lower().strip()
    results = []
    for code, info in AIRPORTS.items():
        if (query in code.lower() or
                query in info["city"].lower() or
                query in info["name"].lower() or
                query in info["country"].lower()):
            results.append({"iata": code, **info})
    return results[:10]


def get_all_iata_codes() -> list[str]:
    """Return all available IATA codes."""
    return sorted(AIRPORTS.keys())
