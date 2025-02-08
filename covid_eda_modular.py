# Databricks notebook source
# MAGIC %md
# MAGIC ### View the latest COVID-19 hospitalization data

# COMMAND ----------

# MAGIC %md
# MAGIC #### Setup 

# COMMAND ----------


import sys
display(sys.version)

# COMMAND ----------

%pip install -r requirements.txt

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

# MAGIC %md
# MAGIC #### Get and Transform data

# COMMAND ----------

from covid_analysis.transforms import *

url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/hospitalizations/covid-hospitalizations.csv"
path = "/tmp/covid-hospitalizations.csv"

get_data(url, path)

# COMMAND ----------

import pandas as pd

# read from /tmp, subset for USA, pivot and fill missing values
df = pd.read_csv("/tmp/covid-hospitalizations.csv")
df = filter_country(df, country='USA')
df = pivot_and_clean(df, fillna=0)  
df = clean_spark_cols(df)
df = index_to_col(df, colname='date')

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Save to Delta Lake
# MAGIC The current schema has spaces in the column names, which are incompatible with Delta Lake.  To save our data as a table, we'll replace the spaces with underscores.  We also need to add the date index as its own column or it won't be available to others who might query this table.

# COMMAND ----------

# Write to Delta Lake
df.to_table(name="dev_covid_trends", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checking the table's and schema available

# COMMAND ----------

# Show available databases
spark.sql("SHOW DATABASES").show()
# Show tables in the current/default database
spark.sql("SHOW TABLES").show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Visualize

# COMMAND ----------

# Using Databricks visualizations and data profiling
display(spark.table("default.dev_covid_trends"))

# COMMAND ----------

# Using python
df.toPandas().plot(figsize=(13,6), grid=True).legend(loc='upper left')

