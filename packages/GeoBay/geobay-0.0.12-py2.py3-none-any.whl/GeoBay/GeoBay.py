"""Main module."""
#ipyleaflet module
from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl
import geopandas as gpd

class CustomIpyleafletMap(IpyleafletMap):
    def __init__(self, center, zoom=12, **kwargs):
        # Initialize the map with the center and zoom parameters
        super().__init__(center=center, zoom=zoom, **kwargs)
        
    def add_basemap(self, basemap_name: str):
        """
        Adds a basemap to the map.

        Parameters:
        - basemap_name (str): The name of the basemap, e.g., "OpenStreetMap", 
          "Esri.WorldImagery", "OpenTopoMap".
        
        Returns:
        - None
        """
        basemap_urls = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Esri.WorldImagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
        }

        if basemap_name not in basemap_urls:
            raise ValueError(f"Basemap '{basemap_name}' is not supported.")

        basemap = TileLayer(url=basemap_urls[basemap_name])
        self.add_layer(basemap)

    def add_layer_control(self):
        """
        Adds a layer control widget to manage layers on the map.

        Returns:
        - None
        """
        control = LayersControl()
        self.add_control(control)

    def add_vector(self, vector_data):
        """
        Adds vector data to the map. Supports formats that can be read by GeoPandas 
        (GeoJSON, Shapefile, etc.).

        Parameters:
        - vector_data (str or GeoDataFrame): File path to a vector dataset 
          (Shapefile, GeoJSON) or a GeoPandas GeoDataFrame.

        Returns:
        - None
        """
        if isinstance(vector_data, str):
            gdf = gpd.read_file(vector_data)
        elif isinstance(vector_data, gpd.GeoDataFrame):
            gdf = vector_data
        else:
            raise ValueError("Input must be a file path or a GeoDataFrame.")

        geo_json_data = gdf.__geo_interface__
        geo_json_layer = GeoJSON(data=geo_json_data)
        self.add_layer(geo_json_layer)

    def show_map(self):
        """
        Displays the ipyleaflet map.
        """
        return self