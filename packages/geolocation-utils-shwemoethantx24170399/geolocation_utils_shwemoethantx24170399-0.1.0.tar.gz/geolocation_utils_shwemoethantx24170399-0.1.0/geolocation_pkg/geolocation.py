from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points in meters."""
    earth_radius = 6371000  # meters
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)
    delta_lat, delta_lon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c

def check_proximity(user_lat, user_lon, target_lat, target_lon, max_distance=50):
    """Check if user is within max_distance (meters) of a target location."""
    return calculate_distance(user_lat, user_lon, target_lat, target_lon) <= max_distance