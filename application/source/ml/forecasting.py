__author__ = "Vitali Muladze"

import warnings
from math import floor
from typing import Iterator

import numpy
import pandas

# Ignore numpy ranking warning
warnings.simplefilter('ignore', numpy.RankWarning)


def forecast_vintages(data_frame: pandas.DataFrame, years: Iterator[int]) -> pandas.DataFrame:
    """
    Forecast compensations per department using past information
    :param data_frame: past information data frame
    :param years: years to forecast
    :return: fore casted data frame
    """
    columns = ["Year", "Department", "Maximum Compensation", "Minimum Compensation", "Average Compensation"]
    forecast_data = pandas.DataFrame(columns=columns)
    for department_name in data_frame["Department"].unique():
        department_data = data_frame[data_frame["Department"] == department_name].sort_values(by="Year")
        department_data.loc[:, "Year"] = department_data["Year"].astype(float)
        _avg = numpy.polyfit(department_data.Year, department_data["avg"], 1)
        _min = numpy.polyfit(department_data.Year, department_data["min"], 1)
        _max = numpy.polyfit(department_data.Year, department_data["max"], 1)
        for year in years:
            b = (year, 1)
            minimum_compensation = floor(numpy.dot(_min, b))
            maximum_compensation = floor(numpy.dot(_max, b))
            average_compensation = floor(numpy.dot(_avg, b))
            results = [year, department_name, maximum_compensation, minimum_compensation, average_compensation]
            data_frame_row = pandas.DataFrame([results], columns=columns)
            forecast_data = pandas.concat([forecast_data, data_frame_row])

    return forecast_data
