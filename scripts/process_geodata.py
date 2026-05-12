import json
import os

def osm_to_geojson(input_path, output_path):
    """
    Simplistic conversion of OSM JSON (from Overpass) to GeoJSON.
    Focuses on 'way' elements with highway tags.
    """
    with open(input_path, 'r') as f:
        osm_data = json.load(f)

    nodes = {node['id']: (node['lon'], node['lat']) for node in osm_data['elements'] if node['type'] == 'node'}
    
    features = []
    for element in osm_data['elements']:
        if element['type'] == 'way' and 'tags' in element and 'highway' in element['tags']:
            coords = []
            valid_way = True
            for node_id in element['nodes']:
                if node_id in nodes:
                    coords.append(nodes[node_id])
                else:
                    # Some nodes might be outside the BBOX if the way crosses it
                    # In a robust implementation, we'd fetch those too, but for now, skip incomplete ways
                    valid_way = False
                    break
            
            if valid_way and len(coords) > 1:
                feature = {
                    "type": "Feature",
                    "properties": element['tags'],
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    }
                }
                features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    print(f"Successfully converted to GeoJSON: {output_path}")
    print(f"Total highway segments processed: {len(features)}")

if __name__ == "__main__":
    input_file = 'data/raw/chandigarh_highways.json'
    output_file = 'data/processed/chandigarh_highways.geojson'
    os.makedirs('data/processed', exist_ok=True)
    if os.path.exists(input_file):
        osm_to_geojson(input_file, output_file)
    else:
        print(f"Input file not found: {input_file}")
