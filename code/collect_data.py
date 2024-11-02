# TO RUN: python collect_data.py ../data/world_cities.csv --output ../data/all_data.json --london_output london_rain.json

import argparse
import json
import pandas as pd
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
        "--london_daily_output",
        default="../data/london_daily_rain.json",
        help="Output JSON file for London's daily data (default: london_daily_rain.json)",
    )
    parser.add_argument(
        "--london_hourly_output",
        default="../data/london_hourly_rain.json",
        help="Output JSON file for London's hourly data (default: london_hourly_rain.json)",
    )
    parser.add_argument(
        "--all_daily_output",
        default="../data/all_daily_rain.json",
        help="Output JSON file for all cities' daily data (default: all_daily_rain.json)",
    )
    parser.add_argument(
        "--all_hourly_output",
        default="../data/all_hourly_rain.json",
        help="Output JSON file for all cities' hourly data (default: all_hourly_rain.json)",
    )
    args = parser.parse_args()

    # Collect data
    results_all = collect_data(args.coord_file)

    # Save London's daily data to CSV
    london_daily_df = pd.DataFrame(results_all["GB,London"]["daily"])
    london_daily_df.to_csv(args.london_daily_output, index=False)
    print(f"London's daily data saved to {args.london_daily_output}")

    # Save London's hourly data to CSV
    london_hourly_df = pd.DataFrame(results_all["GB,London"]["hourly"])
    london_hourly_df.to_csv(args.london_hourly_output, index=False)
    print(f"London's hourly data saved to {args.london_hourly_output}")

    # Save daily data for all cities to CSV
    daily_data = {city: data["daily"] for city, data in results_all.items()}
    all_daily_df = pd.DataFrame.from_dict(daily_data, orient="index")
    all_daily_df.to_csv(args.all_daily_output, index=False)
    print(f"All cities' daily data saved to {args.all_daily_output}")

    # Save hourly data for all cities to CSV
    hourly_data = {city: data["hourly"] for city, data in results_all.items()}
    all_hourly_df = pd.DataFrame.from_dict(hourly_data, orient="index")
    all_hourly_df.to_csv(args.all_hourly_output, index=False)
    print(f"All cities' hourly data saved to {args.all_hourly_output}")


if __name__ == "__main__":
    main()
