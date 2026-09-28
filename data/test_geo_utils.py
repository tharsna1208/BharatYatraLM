from data.geo_utils import calculate_distance


goa_latitude = 15.3000
goa_longitude = 73.8000


distance = calculate_distance(
    goa_latitude,
    goa_longitude,
    goa_latitude,
    goa_longitude
)


print(
    "Distance from Goa to Goa:"
)

print(
    f"{distance:.2f} km"
)