__author__ = "Vitali Muladze"

import pandas
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database

from source.configuration import DataBase


def data_frame_to_html(data_frame: DataFrame) -> str:
    """
    Cast pandas data frame to html
    :param data_frame: data frame to show on web
    :return: data frame to html table
    """
    return data_frame.to_html(float_format="%.2f", index=False,
                              classes=["table table-striped table-sm"])


def insert_into_collection(_db: Database, collection_name: str, data_frame: pandas.DataFrame) -> None:
    """
    Insert given csv files to mongo database
    :param _db: database name, existence is optional
    :param collection_name: collection name, existence is optional
    :param data_frame: data frame to insert into database
    """
    _db[collection_name].drop()
    _db[collection_name].insert_many(data_frame.to_dict('records'))


def insert_csv_files_to_mongo() -> None:
    """
    Parse given csv file
    """
    # Create mongo connection
    mongo_client = MongoClient(DataBase.host, DataBase.port)
    db = mongo_client["flatrock_db"]
    collection_name = "data"
    # Columns map for given file
    columns = {"Employee": "name", "Department": "department", "Job Title/Duties": "job",
               "Compensation in 2012": "compensation"}
    file_data = pandas.read_csv("/data/2012-bloomington-civil-city-anual-compensation.csv")
    file_data = file_data.rename(columns=columns)
    file_data = file_data.drop("City", axis=1)
    file_data.loc[:, "compensation"] = file_data["compensation"].astype(float)
    file_data.loc[:, "year"] = "2012"
    # Columns map for given file
    columns = {"Employee": "name", "Department": "department", "Job Title/Duties": "job",
               "Compensation in 2013": "compensation"}
    temp_data = pandas.read_csv("/data/2013-bloomington-civil-city-anual-compensation.csv")
    temp_data = temp_data.rename(columns=columns)
    temp_data.loc[:, "compensation"] = temp_data["compensation"].astype(float)
    temp_data.loc[:, "year"] = "2013"
    file_data = pandas.concat([file_data, temp_data], sort=True)
    # Columns map for given file
    columns = {"Employee": "name", "Department": "department", "Job Title/Duties": "job",
               "Compensation in 2014": "compensation"}
    temp_data = pandas.read_csv("/data/2014-bloomington-civil-city-anual-compensation.csv")
    temp_data = temp_data.rename(columns=columns)
    temp_data = temp_data.drop("City", axis=1)
    temp_data.loc[:, "compensation"] = temp_data["compensation"].astype(float)
    temp_data.loc[:, "year"] = "2014"
    file_data = pandas.concat([file_data, temp_data], sort=True)
    # Columns map for given file
    columns = {"Employee": "name", "Department": "department", "Job Title/Duties": "job",
               "Compensation in 2015": "compensation"}
    temp_data = pandas.read_csv("/data/2015-bloomington-civil-city-anual-compensation.csv")
    temp_data = temp_data.rename(columns=columns)
    temp_data = temp_data.drop("City", axis=1)
    temp_data.loc[:, "compensation"] = temp_data["compensation"].astype(float)
    temp_data.loc[:, "year"] = "2015"
    file_data = pandas.concat([file_data, temp_data], sort=True)
    # Columns map for given file
    columns = {"first_name": "name", "Department": "department", "job_title": "job",
               "total_compensation": "compensation"}
    temp_data = pandas.read_csv("/data/2016-bloomington-civil-city.csv")
    temp_data = temp_data.rename(columns=columns)
    temp_data = temp_data.drop("Textbox6", axis=1)
    temp_data = temp_data.drop("Textbox14", axis=1)
    temp_data.loc[:, "compensation"] = temp_data["compensation"].apply(lambda x: float(x[1:].replace(",", "")))
    temp_data.loc[:, "year"] = "2016"
    file_data = pandas.concat([file_data, temp_data], sort=True)
    # Columns map for given file
    columns = {"Name": "name", "Department": "department", "Job Title": "job", "Salary": "compensation"}
    temp_data = pandas.read_csv("/data/2017-bloomington-civil-city-annual-compensation.csv")
    temp_data = temp_data.rename(columns=columns)
    temp_data.loc[:, "compensation"] = temp_data["compensation"].apply(lambda x: float(x.replace(",", "")))
    temp_data.loc[:, "year"] = "2017"
    file_data = pandas.concat([file_data, temp_data], sort=True)
    # Insert into database collection
    insert_into_collection(_db=db, collection_name=collection_name, data_frame=file_data)
