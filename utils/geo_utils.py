"""
Geographic utility functions for Krishi Sakhi application.

This module contains functions for:
- Converting acres to radius
- Generating circle polygons for farm boundaries
- Calculating geographic bounds
"""

import math
import numpy as np
from typing import List, Tuple, Dict, Any
from geopy.distance import distance as geopy_distance

def acres_to_radius(acres: float) -> float:
    """
    Convert area in acres to radius in meters for a circular representation.
    
    Formula: 1 acre = 4046.86 square meters
    Circle area: A = π × r²
    Therefore: r = √(A/π)
    
    Args:
        acres (float): Area in acres
        
    Returns:
        float: Radius in meters
        
    Example:
        >>> acres_to_radius(1.0)
        35.918861636371536
    """
    if acres <= 0:
        return 0
    
    # Convert acres to square meters
    area_square_meters = acres * 4046.86
    
    # Calculate radius using circle area formula
    radius_meters = math.sqrt(area_square_meters / math.pi)
    
    return radius_meters

def generate_circle_polygon(lat: float, lng: float, radius_meters: float, num_points: int = 36) -> List[List[float]]:
    """
    Generate a polygon representing a circle for GeoJSON format.
    
    This function creates a series of points around a circle's perimeter
    to approximate the circular farm boundary as a polygon.
    
    Args:
        lat (float): Center latitude in decimal degrees
        lng (float): Center longitude in decimal degrees  
        radius_meters (float): Radius of the circle in meters
        num_points (int): Number of points to generate (default: 36)
        
    Returns:
        List[List[float]]: List of [longitude, latitude] coordinate pairs
        
    Note:
        GeoJSON format requires [longitude, latitude] order, not [latitude, longitude]
    """
    if radius_meters <= 0:
        # Return a single point if radius is zero or negative
        return [[lng, lat]]
    
    points = []
    
    # Calculate the distance per degree at this latitude
    # This is an approximation for small distances
    lat_rad = math.radians(lat)
    meters_per_degree_lat = 111132.92 - 559.82 * math.cos(2 * lat_rad) + 1.175 * math.cos(4 * lat_rad)
    meters_per_degree_lng = 111412.84 * math.cos(lat_rad) - 93.5 * math.cos(3 * lat_rad)
    
    # Generate points around the circle
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Calculate offset in meters
        offset_lat_meters = radius_meters * math.sin(angle)
        offset_lng_meters = radius_meters * math.cos(angle)
        
        # Convert to degrees
        offset_lat_degrees = offset_lat_meters / meters_per_degree_lat
        offset_lng_degrees = offset_lng_meters / meters_per_degree_lng
        
        # Calculate new coordinates
        new_lat = lat + offset_lat_degrees
        new_lng = lng + offset_lng_degrees
        
        # Add to points list (GeoJSON format: [lng, lat])
        points.append([new_lng, new_lat])
    
    # Close the polygon by adding the first point at the end
    if points:
        points.append(points[0])
    
    return points

def calculate_circle_bounds(lat: float, lng: float, radius_meters: float) -> Dict[str, float]:
    """
    Calculate the bounding box for a circle.
    
    Args:
        lat (float): Center latitude
        lng (float): Center longitude
        radius_meters (float): Radius in meters
        
    Returns:
        Dict[str, float]: Dictionary with 'north', 'south', 'east', 'west' bounds
    """
    if radius_meters <= 0:
        return {
            'north': lat,
            'south': lat,
            'east': lng,
            'west': lng
        }
    
    # Calculate approximate degree offsets
    lat_rad = math.radians(lat)
    meters_per_degree_lat = 111132.92 - 559.82 * math.cos(2 * lat_rad) + 1.175 * math.cos(4 * lat_rad)
    meters_per_degree_lng = 111412.84 * math.cos(lat_rad) - 93.5 * math.cos(3 * lat_rad)
    
    lat_offset = radius_meters / meters_per_degree_lat
    lng_offset = radius_meters / meters_per_degree_lng
    
    return {
        'north': lat + lat_offset,
        'south': lat - lat_offset,
        'east': lng + lng_offset,
        'west': lng - lng_offset
    }

def format_coordinates_for_display(lat: float, lng: float) -> str:
    """
    Format coordinates for user-friendly display.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        str: Formatted coordinate string
    """
    return f"{lat:.6f}°N, {lng:.6f}°E"

def validate_kerala_coordinates(lat: float, lng: float) -> bool:
    """
    Check if coordinates fall within Kerala's approximate boundaries.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        bool: True if coordinates are within Kerala bounds
    """
    # Approximate Kerala boundaries
    kerala_bounds = {
        'north': 12.8,
        'south': 8.2,
        'east': 77.4,
        'west': 74.8
    }
    
    return (kerala_bounds['south'] <= lat <= kerala_bounds['north'] and
            kerala_bounds['west'] <= lng <= kerala_bounds['east'])

def calculate_area_from_radius(radius_meters: float) -> float:
    """
    Convert radius in meters back to area in acres.
    
    Args:
        radius_meters (float): Radius in meters
        
    Returns:
        float: Area in acres
    """
    if radius_meters <= 0:
        return 0
    
    # Calculate area in square meters
    area_square_meters = math.pi * (radius_meters ** 2)
    
    # Convert to acres
    acres = area_square_meters / 4046.86
    
    return acres

# Alias for backward compatibility
acres_to_radius_meters = acres_to_radius

def validate_coordinates(lat: float, lng: float) -> bool:
    """
    Validate if coordinates are within reasonable bounds.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        bool: True if coordinates are valid
    """
    return (-90 <= lat <= 90) and (-180 <= lng <= 180)
