__author__ = "Vitali Muladze"

from typing import List

from flask_pymongo import PyMongo
from pandas import DataFrame


def get_data(mongo: PyMongo, pipeline: list, collection: str = "data", _extract_index=False, _drop_index=False,
             index_key="_id") -> DataFrame:
    """
    Function for getting data from mongodb and representing it as data frame
    """
    results = mongo.db[collection].aggregate(pipeline)
    results = list(results)
    if _extract_index:
        results = extract_index(results, index_key=index_key)
    if _drop_index:
        results = drop_index(results, index_key=index_key)
    return DataFrame(results)


def extract_index(results: List[dict], index_key: str = "_id"):
    """
    Extract index from
    :param index_key: index key for query
    :param results: mongo query results
    :return:
    """
    if len(results) == 0:
        return results
    temp_list = list()
    keys = results[0][index_key].keys()
    for item in results:
        for key in keys:
            item[key] = item[index_key][key]

        temp_list.append(item)

    return temp_list


def drop_index(results: List[dict], index_key="_id"):
    temp_list = list()
    for item in results:
        del item[index_key]
        temp_list.append(item)

    return temp_list
