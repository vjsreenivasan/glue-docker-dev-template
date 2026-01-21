"""
Simple AWS Glue Job Template

A minimal Glue job for quick experimentation
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Your ETL logic here
print("Starting Glue Job...")
print(f"Spark Version: {spark.version}")
print(f"Job Name: {args['JOB_NAME']}")

# Example: Create a simple DataFrame
data = [
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Charlie", 35)
]
columns = ["id", "name", "age"]

df = spark.createDataFrame(data, columns)
print("\nSample DataFrame:")
df.show()

print("\nJob completed successfully!")

# Commit the job
job.commit()
