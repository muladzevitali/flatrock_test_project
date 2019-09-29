__author__ = "Vitali Muladze"

from flask import (Blueprint, render_template, request, redirect, url_for)

from apps import mongo
from source.utils import data_frame_to_html, get_data
from source.ml import forecast_vintages
from .forms import (ForecastDateForm, ReportDateForm)
from .queries import *

analytics_app = Blueprint(name="analytics_app", import_name=__name__)


@analytics_app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Get the analytics type from user
        analyse_type = request.args.get("type")
        if analyse_type:
            return redirect(url_for('analytics_app.%s' % analyse_type))

    return render_template("index.html")


@analytics_app.route("/first_analytics", methods=["POST", "GET"])
def first_analytics():
    # Form for getting selected field from user
    form = ReportDateForm(request.form)
    # Output table
    table: None or str = None
    order: list = ["Year", "Maximum Compensation", "Minimum Compensation",
                   "Average Compensation", "Number of Employees"]

    if request.method == "POST" and form.validate_on_submit():
        year = form.years.data
        if year == "all":
            pipeline = [min_max_avg_all_years]
            data_frame = get_data(mongo, pipeline)
            data_frame = data_frame.rename(columns={"_id": "Year"})

        else:
            _filter = {"$match": {"year": year}}
            data_frame = get_data(mongo, pipeline=[_filter, min_max_avg], _drop_index=True, index_key="_id")
            data_frame.loc[:, "Year"] = year

        data_frame = data_frame[order].sort_values(by="Year")
        table = data_frame_to_html(data_frame)

    return render_template("analytics.html", form=form, url=url_for(request.endpoint), table=table)


@analytics_app.route("/second_analytics", methods=["POST", "GET"])
def second_analytics():
    # Form for getting selected field from user
    form = ReportDateForm(request.form)
    # Output table
    table: None or str = None
    # Order of output
    order: list = ["Department", "Year", "Average Compensation", "Number of Employees"]

    if request.method == "POST" and form.validate_on_submit():
        year = form.years.data
        if year == "all":
            # Aggregate the pipeline
            pipeline = [avg_department_year]
            data_frame = get_data(mongo, pipeline, _extract_index=True, _drop_index=True)

            data_frame = data_frame[order].sort_values(by=["Department", "Year"])
        else:
            _filter = {"$match": {"year": year}}
            pipeline = [_filter, avg_department]
            data_frame = get_data(mongo, pipeline=pipeline)
            data_frame = data_frame.rename(columns={"_id": "Department"})
            data_frame.loc[:, "Year"] = year

            data_frame = data_frame[order].sort_values(by="Department")

        # Cast pandas data frame to html
        table = data_frame_to_html(data_frame)

    return render_template("analytics.html", form=form, url=url_for(request.endpoint), table=table)


@analytics_app.route("/third_analytics", methods=["POST", "GET"])
def third_analytics():
    # Form for getting selected field from user
    form = ReportDateForm(request.form)
    # Output table
    table: None or str = None
    # Order of output
    order: list = ["Department", "Job", "Year", "Average Compensation", "Number of Employees"]

    if request.method == "POST" and form.validate_on_submit():
        year = form.years.data

        if year == "all":
            # Aggregate the pipeline
            pipeline = [avg_department_year_job]
            data_frame = get_data(mongo, pipeline=pipeline, _extract_index=True, _drop_index=True)
            # Modify the result data

            data_frame = data_frame[order].sort_values(by=["Department", "Job", "Year"])
        else:
            _filter = {"$match": {"year": year}}
            pipeline = [_filter, avg_department_job]
            data_frame = get_data(mongo, pipeline=pipeline, _extract_index=True, _drop_index=True,)
            data_frame.loc[:, "Year"] = year

            data_frame = data_frame[order].sort_values(by=["Department", "Job", "Year"])

        # Cast pandas data frame to html
        table = data_frame_to_html(data_frame)

    return render_template("analytics.html", form=form, url=url_for(request.endpoint), table=table)


@analytics_app.route("/fourth_analytics", methods=["POST", "GET"])
def fourth_analytics():
    form = ForecastDateForm(request.form)
    table: str or None = None

    if request.method == "POST" and form.validate_on_submit():
        year = form.years.data
        # Aggregate the pipeline
        pipeline = [forecast_avg_min_max_department]
        # Get data from database
        data_frame = get_data(mongo, pipeline=pipeline, _extract_index=True, _drop_index=True)
        if year == "all":
            years_to_predict = range(2018, 2029)
        else:
            years_to_predict = [int(year)]
        # Make prediction
        forecast_data_frame = forecast_vintages(data_frame, years_to_predict)
        table = data_frame_to_html(forecast_data_frame)
    return render_template("analytics.html", form=form, url=url_for(request.endpoint), table=table)
