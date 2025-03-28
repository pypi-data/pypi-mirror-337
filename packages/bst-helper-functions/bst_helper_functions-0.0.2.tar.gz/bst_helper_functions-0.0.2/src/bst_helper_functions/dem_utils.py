import os

import numpy as np
from itertools import product
import rasterio as rio
from rasterio.merge import merge



def convert_agl_to_msl(lon, lat, alt_agl, dem, dem_data):
    terrain_elevation = get_elevation_at_latlon(dem, dem_data, lon, lat)
    return terrain_elevation + alt_agl


def find_high_terrain_within_bounds(bounds, dem, dem_data):
    north_indx, south_indx, west_indx, east_indx = get_dem_subset_indexes(bounds, dem)
    dem_subset = dem_data[north_indx:south_indx, west_indx:east_indx]
    max_elevaton = float(np.amax(dem_subset))
    
    return max_elevaton


def get_dem_subset_indexes(bounds, dem):
    north_indx, west_indx = dem.index(bounds["west"], bounds["north"])
    south_indx, east_indx = dem.index(bounds["east"], bounds["south"])
    
    return (north_indx, south_indx, west_indx, east_indx)


def get_elevation_at_latlon(dem, dem_data, lon, lat):
    row, col = dem.index(lon, lat)
    el = dem_data[row, col]
    return float(el)


def get_elevations_along_path(dem, dem_data, lons, lats):
    els = [get_elevation_at_latlon(dem, dem_data, lon, lat) for lon, lat in zip(lons, lats)]
    
    return els


def get_elevations_vec_from_lons_grid(dem, dem_data, lons_grid, lats_grid):
    els = np.zeros(lons_grid.shape, dtype=float)
    for x, y  in product(range(lons_grid.shape[0]), range(lons_grid.shape[1])):
        els[x, y] = get_elevation_at_latlon(dem, dem_data, lons_grid[x, y], lats_grid[x, y])
    
    return els


def load_dem(self, resources_dir, dem_dir):
        mosaic_list = []
        for file in os.listdir(dem_dir + '/'):
            fp = dem_dir + '/' + file
            data = rio.open(fp)
            mosaic_list.append(fp)
        mosaic, tf = merge(mosaic_list, method='max')
        meta = data.meta.copy()
        meta.update({
            "driver": 'GTiff',
            "height": mosaic.shape[1], 
            "width": mosaic.shape[2],
            "transform": tf
            })
        
        with rio.open(resources_dir + '/' + "temp_dted.geotiff", "w", **meta) as dest:
            dest.write(mosaic)
        dted = rio.open(resources_dir + '/' + "temp_dted.geotiff")
        
        return dted  

# def get_LoS_min_elevations_along_path(dem, dem_data, gcs_location, path_lons, path_lats, LoS_path_check_interval):
#     LoS_min_elevations = []
#     for path_point in zip(path_lons, path_lats):
#         # Get ray lons and lats from GCS location to sample point
#         ray_lons, ray_lats, _, _, _ = plut.segment_path_by_resolution(gcs_location, path_point, LoS_path_check_interval)
#         # Get terrain elevations along ray from GCS location to sample point
#         terrain_els = get_elevations_along_path(dem, dem_data, ray_lons, ray_lats)
#         dist = None
#         highest_slope = -1000.0
#         for lon, lat, el in zip(ray_lons, ray_lats, terrain_els):
#             _, dist = calc_azimuth_dist_btwn_lonlats(gcs_location, (lon, lat))
#             if dist == 0:
#                 continue
#             slope = (el - gcs_location[2]) / dist
#             highest_slope = max(highest_slope, slope)
#         LoS_min_elevations.append((highest_slope * dist) + gcs_location[2])
    
#     return np.asarray(LoS_min_elevations)