import math


def calculate_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):

    
    earth_radius = 6371.0

    
    latitude1 = math.radians(
        latitude1
    )

    longitude1 = math.radians(
        longitude1
    )

    latitude2 = math.radians(
        latitude2
    )

    longitude2 = math.radians(
        longitude2
    )

    
    delta_latitude = (
        latitude2 - latitude1
    )

    delta_longitude = (
        longitude2 - longitude1
    )

    # Haversine formula
    a = (
        math.sin(
            delta_latitude / 2
        ) ** 2
        +
        math.cos(latitude1)
        *
        math.cos(latitude2)
        *
        math.sin(
            delta_longitude / 2
        ) ** 2
    )

    c = (
        2
        *
        math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
    )

    distance = (
        earth_radius * c
    )

    return distance