from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd
import streamlit as st
from pytz import timezone

from parameters import DailyParameters
from weather import Weather


def get_weather_data(
    latitude: float,
    longitude: float,
    wedding_date: datetime,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    weather = Weather(latitude=latitude, longitude=longitude)
    weather_response = weather.get(
        start_date=start_date,
        end_date=end_date,
        timezone=timezone("America/Sao_Paulo"),
        daily_parameters=[
            DailyParameters.temperature_2m_max,
            DailyParameters.temperature_2m_min,
            DailyParameters.rain_sum,
            DailyParameters.precipitation_hours,
            DailyParameters.windspeed_10m_max,
        ],
    ).to_dict()

    weather_df = pd.DataFrame(
        {
            "time": pd.to_datetime(weather_response["daily"]["time"]),
            "temperature_2m_min": weather_response["daily"]["temperature_2m_min"],
            "temperature_2m_max": weather_response["daily"]["temperature_2m_max"],
            "rain_sum": weather_response["daily"]["rain_sum"],
            "precipitation_hours": weather_response["daily"]["precipitation_hours"],
            "windspeed_10m_max": weather_response["daily"]["windspeed_10m_max"],
        }
    )

    return weather_df[
        (weather_df["time"].dt.day == wedding_date.day)
        & (weather_df["time"].dt.month == wedding_date.month)
    ]


def create_text_input() -> Dict[str, Any]:
    st.sidebar.text_input("Latitude", key="latitude", value="-23.0033")
    st.sidebar.text_input("Longitude", key="longitude", value="-49.3219")

    return {
        "latitude": float(st.session_state.latitude),
        "longitude": float(st.session_state.longitude),
    }


def create_date_input() -> Dict[str, Any]:
    st.sidebar.date_input(
        "Wedding Date", key="wedding_date", value=datetime(2024, 5, 4)
    )
    st.sidebar.date_input("Start Date", key="start_date", value=datetime(2000, 1, 1))
    st.sidebar.date_input("End Date", key="end_date", value=datetime(2023, 10, 16))

    return {
        "wedding_date": st.session_state.wedding_date,
        "start_date": st.session_state.start_date,
        "end_date": st.session_state.end_date,
    }


def create_map(column_position, latitude: float, longitude: float):
    df_map = pd.DataFrame(
        {"latitude": np.array([latitude]), "longitude": np.array([longitude])}
    )
    column_position.map(df_map)


def create_temperature_area_chart(wedding_weather_df: pd.DataFrame):
    temperature_df = wedding_weather_df[
        ["temperature_2m_min", "temperature_2m_max", "time"]
    ]
    st.area_chart(
        temperature_df,
        x="time",
        y=["temperature_2m_min", "temperature_2m_max"],
        color=["#FF0000", "#0000FF"],
    )


def create_rain_area_chart(wedding_weather_df: pd.DataFrame):
    rain_df = wedding_weather_df[["precipitation_hours", "time"]]
    st.area_chart(
        rain_df,
        x="time",
        y=["precipitation_hours"],
    )


def create_wind_area_chart(wedding_weather_df: pd.DataFrame):
    wind_df = wedding_weather_df[["windspeed_10m_max", "time"]]
    st.area_chart(
        wind_df,
        x="time",
        y=["windspeed_10m_max"],
    )


def main():
    st.set_page_config(page_title="Weather Wedding", layout="wide")
    text_input_dict = create_text_input()
    date_input_dict = create_date_input()

    if st.sidebar.button("Submit"):
        wedding_weather_df = get_weather_data(
            text_input_dict["latitude"],
            text_input_dict["longitude"],
            date_input_dict["wedding_date"],
            date_input_dict["start_date"],
            date_input_dict["end_date"],
        )

        left_column, right_column = st.columns(2)
        left_column.title("Weather Wedding Stats")
        create_map(
            right_column, text_input_dict["latitude"], text_input_dict["longitude"]
        )

        st.markdown("**Min/Max Temperature**")
        create_temperature_area_chart(wedding_weather_df)

        st.markdown("**Precipitation Hours**")
        create_rain_area_chart(wedding_weather_df)

        st.markdown("**Max Wind**")
        create_wind_area_chart(wedding_weather_df)


if __name__ == "__main__":
    main()
