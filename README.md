1. Run the shopping cart python code (local):

```
cd shop 
python3 main.py
```

2. Run the recipes job with Spark (standalone):

```
cd recipes_etl
spark-submit spark_recipes_job.py --input data/recipes.json --output beefs.parquet
```

3. Run the recipes job with Spark (YARN):

```
cd recipes_etl
spark-submit spark_recipes_job.py --master yarn --deploy-mode client --input data/recipes.json --output beefs.parquet
```
This should be tested on a real cluster!

4. Run the recipes job in a Jupyter notebook:
```
cd recipes_etl
jupyter notebook recipes_notebook.ipynb 
```