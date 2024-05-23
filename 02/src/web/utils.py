from datetime import datetime

import pandas as pd


def get_period_day(date):
    date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").time()
    morning_min = datetime.strptime("05:00", "%H:%M").time()
    morning_max = datetime.strptime("11:59", "%H:%M").time()
    afternoon_min = datetime.strptime("12:00", "%H:%M").time()
    afternoon_max = datetime.strptime("18:59", "%H:%M").time()
    evening_min = datetime.strptime("19:00", "%H:%M").time()
    evening_max = datetime.strptime("23:59", "%H:%M").time()
    night_min = datetime.strptime("00:00", "%H:%M").time()
    night_max = datetime.strptime("04:59", "%H:%M").time()
    if date_time > morning_min and date_time < morning_max:
        return "mañana"
    elif date_time > afternoon_min and date_time < afternoon_max:
        return "tarde"
    elif (
        (date_time > evening_min and date_time < evening_max) or
        (date_time > night_min and date_time < night_max)
    ):
        return "noche"


def is_high_season(fecha):
    fecha_year = int(fecha.split("-")[0])
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    range1_min = datetime.strptime("15-Dec", "%d-%b").replace(year = fecha_year)
    range1_max = datetime.strptime("31-Dec", "%d-%b").replace(year = fecha_year)
    range2_min = datetime.strptime("1-Jan", "%d-%b").replace(year = fecha_year)
    range2_max = datetime.strptime("3-Mar", "%d-%b").replace(year = fecha_year)
    range3_min = datetime.strptime("15-Jul", "%d-%b").replace(year = fecha_year)
    range3_max = datetime.strptime("31-Jul", "%d-%b").replace(year = fecha_year)
    range4_min = datetime.strptime("11-Sep", "%d-%b").replace(year = fecha_year)
    range4_max = datetime.strptime("30-Sep", "%d-%b").replace(year = fecha_year)
    if (
        (fecha >= range1_min and fecha <= range1_max) or
        (fecha >= range2_min and fecha <= range2_max) or
        (fecha >= range3_min and fecha <= range3_max) or
        (fecha >= range4_min and fecha <= range4_max)
    ):
        return 1
    return 0


def normalize(data):
    data["period_day"] = data["Fecha-I"].apply(get_period_day)
    data["high_season"] = data["Fecha-I"].apply(is_high_season)
    features = pd.concat([
        pd.get_dummies(data["OPERA"], prefix="OPERA"),
        pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
        pd.get_dummies(data["MES"], prefix="MES"),
        pd.get_dummies(data["DIANOM"], prefix="DIANOM"),
        pd.get_dummies(data["period_day"], prefix="period_day"),
        data["high_season"],
    ], axis=1)
    top_10_features = [
        "period_day_mañana",
        "period_day_noche",
        "DIANOM_Martes",
        "high_season",
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air"
    ]
    for t in top_10_features:
        if t not in features:
            features[t] = False
    features = features[top_10_features]
    return features