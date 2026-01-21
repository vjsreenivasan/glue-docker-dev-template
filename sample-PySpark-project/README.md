# Sample PySpark Project for AWS Glue

A complete sample project demonstrating AWS Glue ETL jobs using PySpark in a local Docker environment.

## Project Structure

```
sample-PySpark-project/
├── jobs/                      # Glue job scripts
│   ├── sample_etl_job.py     # Full ETL example with transformations
│   └── simple_glue_job.py    # Minimal Glue job template
├── data/
│   ├── input/                # Sample input data
│   │   ├── customers.csv
│   │   └── orders.csv
│   └── output/               # Job output directory
├── scripts/                   # Helper scripts
│   ├── run_glue_job.sh       # Run a Glue job
│   ├── start_jupyter.sh      # Start Jupyter notebook
│   └── start_shell.sh        # Start PySpark shell
├── lib/                      # Custom libraries (optional)
└── README.md
```

## Prerequisites

1. **Docker installed** on your machine
2. **AWS Glue Docker image** pulled:
   ```bash
   docker pull amazon/aws-glue-libs:glue_libs_4.0.0_image_01
   ```

## Quick Start

### 1. Run a Simple Glue Job

Run the simple Glue job to test your setup:

```bash
cd sample-PySpark-project/scripts
./run_glue_job.sh simple_glue_job.py
```

### 2. Run the Full ETL Job

Run the complete ETL example that reads from CSV and writes to Parquet:

```bash
./run_glue_job.sh sample_etl_job.py
```

Check the output in `data/output/` directory.

### 3. Start Jupyter Notebook

For interactive development:

```bash
./start_jupyter.sh
```

Then open your browser to `http://localhost:8888` and use the token displayed in the terminal.

### 4. Start PySpark Shell

For quick testing:

```bash
./start_shell.sh
```

## Sample Jobs Explained

### simple_glue_job.py

A minimal Glue job that demonstrates:
- Job initialization
- Creating a simple DataFrame
- Basic PySpark operations

Perfect for testing your environment setup.

### sample_etl_job.py

A complete ETL job that demonstrates:
- Reading CSV data using Glue DynamicFrame
- Data transformations (uppercase, concatenation, filtering)
- Field mapping and type conversions
- Writing partitioned Parquet output
- Error handling and logging

## Developing Your Own Jobs

### Basic Job Template

```python
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

# Your transformations
# ...

# Commit the job
job.commit()
```

### Adding Custom Parameters

To pass custom parameters to your job:

1. Add parameters to `getResolvedOptions()`:
   ```python
   args = getResolvedOptions(sys.argv, ['JOB_NAME', 'my_param'])
   ```

2. Update the run script to pass the parameter:
   ```bash
   --my_param="value"
   ```

## Common Operations

### Reading Data

#### From CSV:
```python
datasource = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [input_path], "recurse": True}
)
```

#### From JSON:
```python
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": [input_path], "recurse": True}
)
```

#### From Parquet:
```python
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="parquet",
    connection_options={"paths": [input_path], "recurse": True}
)
```

### Transformations

#### Convert DynamicFrame to DataFrame:
```python
df = dynamic_frame.toDF()
```

#### Apply transformations:
```python
from pyspark.sql.functions import col, upper, concat_ws

df_transformed = df \
    .withColumn("name", upper(col("name"))) \
    .filter(col("name").isNotNull()) \
    .dropDuplicates()
```

#### Convert back to DynamicFrame:
```python
dynamic_frame = DynamicFrame.fromDF(df_transformed, glueContext, "name")
```

#### Apply field mapping:
```python
applymapping = ApplyMapping.apply(
    frame=dynamic_frame,
    mappings=[
        ("old_field", "string", "new_field", "string"),
        ("id", "string", "id", "long")
    ]
)
```

### Writing Data

#### To Parquet:
```python
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    format="parquet",
    connection_options={"path": output_path, "partitionKeys": ["year", "month"]}
)
```

#### To JSON:
```python
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    format="json",
    connection_options={"path": output_path}
)
```

## Troubleshooting

### Docker Image Issues

If the Docker image fails to run:
```bash
docker pull amazon/aws-glue-libs:glue_libs_4.0.0_image_01
```

### Permission Denied on Scripts

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Output Directory Issues

Ensure the output directory exists and has write permissions:
```bash
mkdir -p data/output
```

## Advanced Usage

### Using Custom Libraries

Place your custom Python modules in the `lib/` directory. They will be automatically included via the `--py-files` parameter.

Example:
```python
# lib/my_utils.py
def my_function():
    return "Hello from custom lib"

# In your job:
from my_utils import my_function
print(my_function())
```

### Testing with Different Spark Configurations

Modify the `run_glue_job.sh` script to add Spark configurations:

```bash
spark-submit \
    --conf spark.driver.memory=4g \
    --conf spark.executor.memory=4g \
    /home/glue_user/workspace/jobs/${JOB_SCRIPT}
```

### Debugging

Enable verbose logging in your job:

```python
sc.setLogLevel("INFO")  # or "DEBUG"
```

## Additional Resources

- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/)
- [AWS Glue PySpark Extensions](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [AWS Glue Docker Setup](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html)

## Contributing

Feel free to add more example jobs and utilities to this project!

## License

This is a sample project for learning purposes.
