import argparse
import logging
import os
import shutil
import isodate

from pyspark import SparkContext
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import lit, udf


def parse_file_paths():
    """
        Spark submit command line arguments format: <FILE>.py --input <INPUT> --output <OUTPUT>
    :return: input and output file paths
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="An json input file with recipes.")
    parser.add_argument("--output", help="An parquet output file path for results.")
    args = parser.parse_args()
    if not args.input or not args.output: exit(-1)
    return os.path.abspath(args.input), os.path.abspath(args.output)


def parse_isoduration(iso_duration):
    """author: Ed Finkler"""
    """parse the given iso8601 duration string into a python timedelta object"""
    delta = None
    try:
        delta = isodate.parse_duration(iso_duration)
    except Exception as e:
        logging.warning(e.message)

    return delta


@udf(returnType=BooleanType())
def contains_ingredient(recipe, ingredient):
    if recipe is not None:
        return ingredient in recipe.lower()
    return False


@udf
def compute_dificulty(prepTime, cookTime):
    prepTime = parse_isoduration(prepTime)
    cookTime = parse_isoduration(cookTime)
    total = prepTime.seconds / 60.00 + cookTime.seconds / 60.00
    if total < 30.00:
        return "Easy"
    if 30.00 <= total <= 60.00:
        return "Medium"
    if total > 60.00:
        return "Hard"
    return "Unknown"


if __name__ == '__main__':

    # cmd line args
    in_path, out_path = parse_file_paths()

    # remove previous hadoop file (directory) if already exists
    if os.path.isdir(out_path):
        shutil.rmtree(out_path)

    sc = SparkContext("local[*]", "SparkRecipesJob").getOrCreate()
    sqlc = SQLContext(sc)

    recipes_df = sqlc.read.json(in_path).cache()

    beef_recipes_df = recipes_df \
        .filter(contains_ingredient('ingredients', lit('beef'))) \
        .withColumn('difficulty', compute_dificulty('prepTime', 'cookTime'))

    print("Number of recipes that require beef as ingredient:", beef_recipes_df.count())

    beef_recipes_df.write.parquet(out_path)
