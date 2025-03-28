import numpy as np
import pyproj as pj
from itertools import product



def calc_azimuth_dist_btwn_lonlats(lonlat1, lonlat2):
    # Returns the azimuth and distance, in meters, between the two points in degrees (from North?  need to confirm this)
    geod = pj.Geod(ellps='WGS84')
    az, back_az, dist = geod.inv(lonlat1[0], lonlat1[1], lonlat2[0], lonlat2[1])
    
    return az, dist


def calc_meters_per_deg_lonlat(init_lat):
    phi0 = np.radians(init_lat)
    m_per_deg_lat = 111132.92 - (559.82 * np.cos(2*phi0)) + (1.175 * np.cos(4*phi0)) - (0.0023 * np.cos(6*phi0))
    m_per_deg_lon = (111412.84 * np.cos(phi0)) - (93.5 * np.cos(3*phi0)) + (0.118 * np.cos(5*phi0))
    
    return [m_per_deg_lon, m_per_deg_lat]


def calc_xy_from_lonlats(init_pos, target_pos):
    az, dist = calc_azimuth_dist_btwn_lonlats(init_pos, target_pos)
    az = convert_azimuth_to_cartesian_angle(az)
    x = dist * np.cos((az * np.pi)/180.0)
    y = dist * np.sin((az * np.pi)/180.0)    
    
    return (x, y)


def convert_azimuth_to_cartesian_angle(angle_degrees):
    # We need to 1) reverse the direction of angle measurement (360-x), and 2) subtract 270 degrees, since geometric functions measure counterclockwise from positive x-axis and WGS84 measures clockwise from North.
    az = 360.0 - angle_degrees - 270.0 
    az = wrap_direction_in_radians(az)        
        
    return az


def convert_cartesian_angle_to_azimuth(angle_degrees):
    # We need to 1) reverse the direction of angle measurement (360-x), and 2) add 90 degrees, since geometric functions measure counterclockwise from positive x-axis and WGS84 measures clockwise from North.
    az = 360.0 - angle_degrees + 90.0
    az = wrap_direction_in_degrees(az)       
        
    return az


def convert_cartesian_to_polar(x, y, angle_reference, angle_units):
    r = np.linalg.norm((x, y))
    az = np.arctan2(y, x)
    if angle_reference == "WGS84":
        az = convert_cartesian_angle_to_azimuth(np.degrees(az))
    else:
        pass 
    if angle_units in set(["rads", "radians"]):
        az = np.radians(az)
    else:
        pass
    
    return az, r


def heading_vector_to_components(heading, speed_mps): 
    # Inputs:
        # heading: heading in degrees True
        # speed_mps: speed in meters per second
    # Returns: 
        # easting_component_mps: speed along East-West direction in meters per second
        # northing_component_mps: speed along North-East direction in meters per second
    
    cartesian_angle_rads = np.radians(convert_azimuth_to_cartesian_angle(heading))
    easting_component_mps = speed_mps * np.cos(cartesian_angle_rads)
    northing_component_mps = speed_mps * np.sin(cartesian_angle_rads)
    
    return [easting_component_mps, northing_component_mps]


def invert_azimuth_degrees(az):
    new_az = az + 180.0
    if new_az > 360.0:
        new_az -= 360.0
    return new_az  


def wrap_direction_in_degrees(direction):
    if direction < 0.0:
        direction = 360.0 + direction
    elif direction > 360.0:
        direction = direction - 360.0
    
    return direction


def wrap_direction_in_radians(direction):
    if direction < 0.0:
        direction = (2 * np.pi) + direction
    elif direction > (2 * np.pi):
        direction = direction - (2 * np.pi)
    
    return direction

