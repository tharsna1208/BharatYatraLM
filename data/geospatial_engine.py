import pandas as pd

from data.geo_utils import calculate_distance


class GeospatialEngine:

    def __init__(
        self,
        features_path="notebooks/features.csv"
    ):

        self.data = pd.read_csv(
            features_path
        )

        self.data[
            "latitude"
        ] = pd.to_numeric(
            self.data["latitude"]
        )

        self.data[
            "longitude"
        ] = pd.to_numeric(
            self.data["longitude"]
        )


    def find_nearby(
        self,
        destination_name,
        radius_km=300,
        top_k=10
    ):

        matches = self.data[
            self.data[
                "destination_name"
            ].str.lower()
            == destination_name.lower()
        ]


        if matches.empty:

            return {
                "status": "destination_not_found",

                "destination": destination_name,

                "results": []
            }


        reference = matches.iloc[0]


        reference_latitude = float(
            reference["latitude"]
        )

        reference_longitude = float(
            reference["longitude"]
        )


        nearby_destinations = []

        seen_destinations = set()


        for _, row in self.data.iterrows():

            destination = (
                row["destination_name"]
            )


            if (
                destination.lower()
                == destination_name.lower()
            ):
                continue


            if (
                destination
                in seen_destinations
            ):
                continue


            distance = calculate_distance(

                reference_latitude,
                reference_longitude,

                float(row["latitude"]),
                float(row["longitude"])
            )


            if distance <= radius_km:

                nearby_destinations.append({

                    "destination_name":
                        destination,

                    "distance_km":
                        distance,

                    "latitude":
                        float(
                            row["latitude"]
                        ),

                    "longitude":
                        float(
                            row["longitude"]
                        )
                })


                seen_destinations.add(
                    destination
                )


        nearby_destinations.sort(
            key=lambda item:
                item["distance_km"]
        )


        nearby_destinations = (
            nearby_destinations[
                :top_k
            ]
        )


        if not nearby_destinations:

            return {
                "status": "no_destinations_found",

                "destination": destination_name,

                "radius_km": radius_km,

                "results": []
            }


        return {
            "status": "success",

            "destination": destination_name,

            "radius_km": radius_km,

            "results": nearby_destinations
        }


    def find_nearest(
        self,
        destination_name,
        top_k=5
    ):

        result = self.find_nearby(

            destination_name=destination_name,

            radius_km=float("inf"),

            top_k=top_k
        )


        return result