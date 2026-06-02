import pystac_client
import planetary_computer
import odc.stac
import xarray as xr
import geopandas as gpd

def stream_satellite_cube(gdf: gpd.GeoDataFrame, start_date: str, end_date: str) -> xr.Dataset:

    
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace
    )

    bbox = gdf.total_bounds

    # sending the order in of what we want but not actually loading it. (sending metadata but not recieving data until we are ready)
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox = bbox,
        datetime=f"{start_date}/{end_date}",
        query={"eo:cloud_cover" : {"lt" : 10}}
    )
    items = list(search.get_items())

    #stac.load is loading the data we searched for above (cause now we want it)
    #chunks is lazy evaluation (from haskell) would take up too much room if we allocated memory prior to needing it
    #using xarray instead of arrays to give labels and so it only performs calcs on what we are working with like a specific date and not doing it for every single element in array
    ds = odc.stac.load(
        items,
        bands=["B04", "B08"],
        bbox=bbox,
        resolution=10,
        chunks={"x": 256, "y": 256}
    )

    ds["B04"] = ((ds["B04"].astype("float32") - 1000) / 10000.0).clip(min=0)
    ds["B08"] = ((ds["B08"].astype("float32") - 1000) / 10000.0).clip(min=0)
    return ds