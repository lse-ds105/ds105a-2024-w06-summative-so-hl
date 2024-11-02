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
        default="../data/london_daily_rain.csv",
        help="Output CSV file for London's daily data (default: london_daily_rain.csv)",
    )
    parser.add_argument(
        "--london_hourly_output",
        default="../data/london_hourly_rain.csv",
        help="Output CSV file for London's hourly data (default: london_hourly_rain.csv)",
    )
    parser.add_argument(
        "--all_daily_output",
        default="../data/all_daily_rain.csv",
        help="Output CSV file for all cities' daily data (default: all_daily_rain.csv)",
    )
    parser.add_argument(
        "--all_hourly_output",
        default="../data/all_hourly_rain.csv",
        help="Output CSV file for all cities' hourly data (default: all_hourly_rain.csv)",
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

    # Collect daily data for all cities to DataFrame
    daily_dataframes = []
    for city, data in results_all.items():
        daily_df = pd.DataFrame(data["daily"])
        daily_df["city"] = city
        daily_dataframes.append(daily_df)
    all_daily_df = pd.concat(daily_dataframes, ignore_index=True)

    # Pivot DataFrame to have a separate column for each city's rainfall
    all_daily_pivot = all_daily_df.pivot(index="time", columns="city", values="rain_sum").reset_index()

    # Save daily data for all cities to CSV
    all_daily_pivot.to_csv(args.all_daily_output, index=False)
    print(f"All cities' daily data saved to {args.all_daily_output}")

    # Collect hourly data for all cities to DataFrame
    hourly_dataframes = []
    for city, data in results_all.items():
        hourly_df = pd.DataFrame(data["hourly"])
        hourly_df["city"] = city
        hourly_dataframes.append(hourly_df)
    all_hourly_df = pd.concat(hourly_dataframes, ignore_index=True)

    # Pivot DataFrame to have a separate column for each city's rainfall
    all_hourly_pivot = all_hourly_df.pivot(index="time", columns="city", values="rain").reset_index()

    # Save hourly data for all cities to CSV
    all_hourly_pivot.to_csv(args.all_hourly_output, index=False)
    print(f"All cities' hourly data saved to {args.all_hourly_output}")

if __name__ == "__main__":
    main()
