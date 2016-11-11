import unittest
import sys
from collections import OrderedDict
import re

import pandas
import yaml
from sqlalchemy import create_engine

def _int(x):
    try:
        return int(x)
    except:
        return None

def _float(x):
    try:
        return float(x)
    except:
        return None

def timestamp(x):
    try:
        return int(x)
    except:
        numbers = re.match(r"(\d+)\.(\d{3,3})", x)
        return int("{}{}".format(*numbers.groups()))

def load_mapping(file_name):
    # from a yaml file, it loads the expected mapping. A yaml file look likes :
    # frame.len : int
    # frame.time_epoch : timestamp
    # ip.src : str
    # ip.dst : str
    #
    # if return an OrderedDict where the keey if the metadata name
    # and the value is the function to convert.
    with open(file_name) as f:
        data = yaml.load(f)

    output = OrderedDict()
    for k, v in data.items():
        if v == "int":
            output[k] = _int
        elif v == "float":
            output[k] = _float
        elif v == "str":
            output[k] = str
        elif v == "timestamp":
            output[k] = timestamp
        else:
            raise Exception("value {} in key {} is invalid".format(v, k))

    return output

if __name__ == "__main__":
    mapping = load_mapping(sys.argv[1])
    address = sys.argv[2]
    engine = create_engine("sqlite:///" + address)
    connection = engine.connect()

    for csvfile in sys.argv[3:]:
        sys.stdout.write("{} ... ".format(csvfile))
        # load the csv file as a panda dataframe. The convertion is done there
        try:
            matrix = pandas.read_csv(csvfile, converters=mapping)
        except:
            print("failed (can't parse the csv file)")
            continue

        # removing columns that are not present in the mapping
        for k in set(matrix.columns.values) - set(mapping.keys()):
            matrix = matrix.drop(k, 1)

        # dump the result within a sqlitebase
        try:
            matrix.to_sql("meta", connection, if_exists="append")
            print("done")
        except:
            print("failed (can't insert in database)")

    connection.close()
