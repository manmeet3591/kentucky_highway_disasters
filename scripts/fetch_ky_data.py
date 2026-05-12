import requests
import json
import os

# Kentucky Bounding Box (Approximate for the whole state)
# south, west, north, east
BBOX = "36.49,-89.57,39.15,-81.96"

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

def fetch_ky_highways():
    """
    Fetches major highway geometries in Kentucky using Overpass API.
    """
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"motorway|trunk"]({BBOX});
    );
    out body;
    >;
    out skel qt;
    """
    
    headers = {
        'User-Agent': 'KY-Highway-Disaster-Project/1.0 (manmeet.singh@example.com)',
        'Accept': 'application/json'
    }
    
    print(f"Fetching Kentucky highway data...")
    try:
        response = requests.get(OVERPASS_URL, params={'data': query}, headers=headers)
        response.raise_for_status()
        
        os.makedirs('data/raw', exist_ok=True)
        file_path = 'data/raw/kentucky_highways.json'
        with open(file_path, 'w') as f:
            f.write(response.text)
        print(f"Successfully saved Kentucky highway data to {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_ky_highways()
