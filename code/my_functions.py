import csv
import requests
import calendar
import pandas as pd

# Define constants
NUMBER_YEARS = 5


# Function to extract coordinates
def extract_coord(file, cities_all_dict, coord_all_dict):
    with open(file, "r") as file:
        reader = csv.reader(file)
        city_coords = {f"{row[0]},{row[1]}": [row[2], row[3]] for row in reader}

        for region, cities in cities_all_dict.items():
            if region not in coord_all_dict:
                coord_all_dict[region] = {}

            for city in cities:
                if city in city_coords:
                    coord_all_dict[region][city] = city_coords[city]
    return coord_all_dict


# Function to retrieve daily and hourly rain data
def get_rain_data(latitude, longitude):
    # URL format(day): https://archive-api.open-meteo.com/v1/archive?latitude=-25&longitude=135&start_date=2019-01-01&end_date=2023-12-31&daily=rain_sum
    # URL format(hourly): https://archive-api.open-meteo.com/v1/archive?latitude=51.5085&longitude=-0.1257&start_date=2024-10-12&end_date=2024-10-26&hourly=rain
    start_url = "https://archive-api.open-meteo.com/v1/archive?"
    param_lat_long = "latitude=" + str(latitude) + "&longitude=" + str(longitude)
    time_period = "&start_date=2019-01-01&end_date=2023-12-31"
    end_url = {"daily": "&daily=rain_sum", "hourly": "&hourly=rain"}

    urls = {}
    responses = {}

    for key, end in end_url.items():
        urls[key] = start_url + param_lat_long + time_period + end
        responses[key] = requests.get(urls[key])

    rain_data_daily = responses["daily"].json()
    rain_data_hourly = responses["hourly"].json()

    return rain_data_daily, rain_data_hourly


# Function to take the average of values in dictionary
def ave_rain(data, CONSTANT):
    return {month: round(rain / CONSTANT, 1) for month, rain in data.items()}


# Function to take average of periodic rainfall
def periodic_rain_amt(time, rain_sum, month_true):
    # Initialise empty dictionary
    periodic_rain_sum = {}

    # Group by month (separate years)
    for date, rain in zip(time, rain_sum):
        if month_true:
            date = date.split("-")[1]

        if date not in periodic_rain_sum:
            periodic_rain_sum[date] = rain
        else:
            periodic_rain_sum[date] += rain

    # Take the average
    periodic_rain_ave = ave_rain(periodic_rain_sum, NUMBER_YEARS)

    # Convert month numbers into words
    if month_true:
        periodic_rain_ave = {
            calendar.month_name[int(month)]: amount
            for month, amount in periodic_rain_sum.items()
        }

    return periodic_rain_ave


# Function to find the sum of values of other cities
def add_cities(data):
    save_dict = {}
    for rain in data.values():
        for time, values in rain.items():
            if time not in save_dict:
                save_dict[time] = values
            else:
                save_dict[time] += values
    return save_dict


# Function to match city to region
def match_city_to_region(city, cities_dict):
    return next(region for region, cities in cities_dict.items() if city in cities)


# Function to average regional rain
def ave_regional_rain(data):
    regional_rain_ave = {}
    for region, cities in data.items():
        num_cities = len(cities)
        daily_total = add_cities(cities)
        regional_rain_ave[region] = ave_rain(daily_total, num_cities)
    return regional_rain_ave


# Function to create dataframes for each reigon
def create_region_dfs(ave_data, x_axis):
    region_dfs = {}

    for region, data in ave_data.items():
        df = pd.DataFrame(
            {
                x_axis: list(data.keys()),
                "Rainfall": list(data.values()),
                "Source": "Average city in " + region,
            }
        )

        region_dfs[region] = df
    return region_dfs


# Function to calculate seasonal rain from monthly rain
def calculate_seasonal_rain(monthly_rain):
    seasons = {
        "Winter": ["December", "January", "February"],
        "Spring": ["March", "April", "May"],
        "Summer": ["June", "July", "August"],
        "Autumn": ["September", "October", "November"],
    }

    monthly_rain["Season"] = monthly_rain["Month"].apply(
        lambda month: next(
            (season for season, months in seasons.items() if month in months), None
        )
    )
    seasonal_rain = (
        monthly_rain.groupby(["Season", "Source"])["Rainfall"].sum().reset_index()
    )
    return seasonal_rain
