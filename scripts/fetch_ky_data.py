import requests
import json
import os

# Kentucky Bounding Box (Approximate for the whole state)
# south, west, north, east
BBOX = "36.49,-89.57,39.15,-81.96"

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

def fetch_ky_highways():
    """
    Fetches major highway geometries in Kentucky using Overpass API.
    """
    # Simple query
    query = f"""[out:json][timeout:180];way["highway"~"motorway|trunk"]({BBOX});out body;>;out skel qt;"""
    
    print(f"Fetching Kentucky highway data from Kumi Systems mirror...")
    try:
        response = requests.get(OVERPASS_URL, params={'data': query}, timeout=180)
        response.raise_for_status()
        
        os.makedirs('data/raw', exist_ok=True)
        file_path = 'data/raw/kentucky_highways.json'
        with open(file_path, 'w') as f:
            f.write(response.text)
        print(f"Successfully saved Kentucky highway data to {file_path}")
    except Exception as e:
        print(f"Error fetching Kentucky data: {e}")



if __name__ == "__main__":
    fetch_ky_highways()
