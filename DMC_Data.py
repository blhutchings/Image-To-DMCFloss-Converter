from ColourTransformation import rgb_to_hsv
import pandas as pd
import time
from os import path

URL = "https://dmc.crazyartzone.com/"


def get_dmc_table(url):
    tables = pd.read_html(url)
    dmc_table = tables[0]
    dmc_table["RGB"] = list(zip(dmc_table["Red"], dmc_table["Green"], dmc_table["Blue"]))
    dmc_table.drop(columns="Color", inplace=True)
    dmc_table.drop(columns="Red", inplace=True)
    dmc_table.drop(columns="Green", inplace=True)
    dmc_table.drop(columns="Blue", inplace=True)
    dmc_table.drop(columns="Hex Code", inplace=True)
    gimpHSV_values = []
    opencvHSV_values = []

    for i in range(0, len(dmc_table)):
        r, g, b = dmc_table["RGB"].values[i]
        gimpH, gimpS, gimpV = rgb_to_hsv(r, g, b)
        gimpHSV_values.append((gimpH, gimpS, gimpV))

        opencvH = gimpH / 2
        opencvS = (gimpS / 100) * 255
        opencvV = (gimpV / 100) * 255
        opencvHSV_values.append((opencvH, opencvS, opencvV))

    dmc_table["gimpHSV"] = gimpHSV_values
    dmc_table["opencvHSV"] = opencvHSV_values
    print(dmc_table)
    return dmc_table


def update(name="table.csv"):
    # If does not exist or if it does, check if it is older than a day: Both creates new
    if (not path.exists(name)) or (path.getatime(name) < time.time() - 86400):
        print("Creating or updating database...")
        dmc_table = get_dmc_table(URL)
        dmc_table.to_csv(name, index=False)
