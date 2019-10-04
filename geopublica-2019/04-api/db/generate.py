from utils.packages.extract import extract
from utils.packages.create import tables, tuples
from postgres import Postgres
import subprocess
import argparse
import pandas
import json


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-z",
    "--zip-tables",
    required=True,
    help="path to input tables of database zip",
)
ap.add_argument(
    "-s",
    "--file-structure",
    required=True,
    help="path to input file with database structure",
)
ap.add_argument(
    "-o",
    "--path-out",
    required=True,
    help="path to output folder with database tables in csv",
)
args = vars(ap.parse_args())

# generates the path for output
path_out = args["path_out"]


post = Postgres()


# EXTRAXT ZIP FILES
extract(args["zip_tables"], path_out)

# CREATE TABLES
structure = json.loads(open(args["file_structure"], "r").read())
tables(path_out, structure, post.con)


# Get all
tables_files = subprocess.os.listdir(path_out)
tables_files = list(filter(lambda x: x.split(".")[-1] == "csv", tables_files))
# Get all path of tables
path_tables_files = list(map(lambda x: f"{path_out}/{x}", tables_files))


# ADDS TUPLES
# Adds tuples of states
path_tables_files.remove(f"{path_out}/states.csv")
states = pandas.read_csv(f"{path_out}/states.csv", delimiter=",", header=None)
tuples({"estado": structure["estado"]}, states.values, post.con)

# Adds tuples of cities
path_tables_files.remove(f"{path_out}/cities.csv")
cities = pandas.read_csv(f"{path_out}/cities.csv", delimiter=",", header=None)
tuples({"cidade": structure["cidade"]}, cities.values, post.con)

# Adds tuples of places
for ptf in path_tables_files:
    places = pandas.read_csv(ptf, delimiter=",", header=None)
    out = ptf.split("/")[-1]
    tuples({"cep": structure["cep"]}, places.values, post.con)

post.close()
