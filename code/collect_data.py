# TO RUN: python collect_data.py ../data/world_cities.csv --output ../data/all_data.json --london_output ../data/london_rain.json

import argparse
import json
import my_functions

# Load cities data
with open("../data/cities_config.json", "r") as file:
    cities_all = json.load(file)

# Define coordinates for London
coord_london = [51.50853, -0.12574]


def collect_data(coord_file):
    # Initialize coordinates for cities
    coord_all = my_functions.extract_coord(coord_file, cities_all, {})

    # Initialize results dictionary
    results_all = {}

    # Store results for London
    rain_data_london_daily, rain_data_london_hourly = my_functions.get_rain_data(
        coord_london[0], coord_london[1]
    )
    results_all["GB,London"] = {
        "daily": rain_data_london_daily["daily"],
        "hourly": rain_data_london_hourly["hourly"],
    }

    # Store results for other cities
    for cities in coord_all.values():
        for city, coord in cities.items():
            lat = float(coord[0])
            long = float(coord[1])
            rain_data_daily, rain_data_hourly = my_functions.get_rain_data(lat, long)
            results_all[city] = {
                "daily": rain_data_daily["daily"],
                "hourly": rain_data_hourly["hourly"],
            }

    return results_all


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Collect rainfall data for London and other cities."
    )
    parser.add_argument(
        "coord_file", help="Path to the CSV file containing city coordinates."
    )
    parser.add_argument(
        "--output",
        default="../data/all_data.json",
        help="Output JSON file for all data (default: all_data.json)",
    )
    parser.add_argument(
        "--london_output",
        default="../data/london_rain.json",
        help="Output JSON file for London's data (default: london_rain.json)",
    )
    args = parser.parse_args()

    # Collect data
    results_all = collect_data(args.coord_file)

    # Save full data
    with open(args.output, "w") as file:
        json.dump(results_all, file)
    print(f"All data saved to ../data/{args.output}")

    # Save London data
    london_data = results_all["GB,London"]
    with open(args.london_output, "w") as file:
        json.dump(london_data, file)
    print(f"London's data saved to ../data/{args.london_output}")


if __name__ == "__main__":
    main()
