"""
Sample AWS Glue ETL Job using PySpark

This job demonstrates:
- Reading data from a source (CSV)
- Transforming data using Glue DynamicFrame
- Writing data to a destination (Parquet)
"""

import sys
import os

# Ensure lib modules are visible
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
try:
    import glue_utils
    glue_utils.init_debugger()
except ImportError:
    print("Warning: glue_utils not found, debugger init skipped.")

from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, upper, concat_ws, to_date


# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Log job parameters
print(f"Job Name: {args['JOB_NAME']}")
print(f"Input Path: {args['input_path']}")
print(f"Output Path: {args['output_path']}")


def read_source_data(glue_context, input_path):
    """
    Read source data as a Glue DynamicFrame
    """
    print(f"Reading data from: {input_path}")
    
    # Read CSV data
    datasource = glue_context.create_dynamic_frame.from_options(
        format_options={
            "quoteChar": '"',
            "withHeader": True,
            "separator": ","
        },
        connection_type="s3",
        format="csv",
        connection_options={
            "paths": [input_path],
            "recurse": True
        },
        transformation_ctx="datasource"
    )
    
    print(f"Record count: {datasource.count()}")
    print("Schema:")
    datasource.printSchema()
    
    return datasource


def transform_data(dynamic_frame):
    """
    Apply transformations to the data
    """
    print("Applying transformations...")
    
    # Convert DynamicFrame to DataFrame for complex transformations
    df = dynamic_frame.toDF()
    
    # Example transformations:
    # 1. Convert name to uppercase
    # 2. Create a full_name column
    # 3. Filter out records with null values
    # 4. Convert string date to date type
    
    df_transformed = df \
        .withColumn("name", upper(col("name"))) \
        .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
        .filter(col("name").isNotNull()) \
        .dropDuplicates()
    
    # Convert back to DynamicFrame
    dynamic_frame_transformed = DynamicFrame.fromDF(
        df_transformed, 
        glueContext, 
        "dynamic_frame_transformed"
    )
    
    print(f"Transformed record count: {dynamic_frame_transformed.count()}")
    
    return dynamic_frame_transformed


def apply_mapping(dynamic_frame):
    """
    Apply field mappings and data type conversions
    """
    print("Applying field mappings...")
    
    # Example: Map fields and change data types
    applymapping = ApplyMapping.apply(
        frame=dynamic_frame,
        mappings=[
            ("id", "string", "customer_id", "long"),
            ("name", "string", "customer_name", "string"),
            ("email", "string", "email_address", "string"),
            ("age", "string", "age", "int"),
            ("city", "string", "city", "string"),
            ("country", "string", "country", "string")
        ],
        transformation_ctx="applymapping"
    )
    
    return applymapping


def write_output_data(glue_context, dynamic_frame, output_path):
    """
    Write transformed data to destination
    """
    print(f"Writing data to: {output_path}")
    
    # Write as Parquet format
    datasink = glue_context.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        format="parquet",
        connection_options={
            "path": output_path,
            "partitionKeys": ["country"]  # Partition by country
        },
        transformation_ctx="datasink"
    )
    
    print("Data write completed successfully")
    
    return datasink


# Main ETL logic
try:
    # Step 1: Read source data
    source_data = read_source_data(glueContext, args['input_path'])
    
    # Step 2: Transform data
    transformed_data = transform_data(source_data)
    
    # Step 3: Apply field mappings
    mapped_data = apply_mapping(transformed_data)
    
    # Step 4: Write to destination
    write_output_data(glueContext, mapped_data, args['output_path'])
    
    print("Job completed successfully!")
    
except Exception as e:
    print(f"Job failed with error: {str(e)}")
    raise e

finally:
    # Commit the job
    job.commit()
