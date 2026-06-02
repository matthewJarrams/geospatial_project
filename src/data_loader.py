import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

def get_alberta_fields() -> gpd.GeoDataFrame:

    coordinates = [
        [-113.117294, 49.771035],
        [-113.095665, 49.771256],
        [-113.095493, 49.757512],
        [-113.116951, 49.757623],
        [-113.117294, 49.771035]
    ]

    poly = Polygon(coordinates)


    gdf = gpd.GeoDataFrame(
        {"field_group_id": ["lethbridge_block_01"]}, 
        geometry=[poly], 
        crs="EPSG:4326"
    )
    
    print(f"Successfully initialized spatial box layer (from collab).")
    return gdf
