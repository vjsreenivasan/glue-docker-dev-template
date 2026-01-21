# Sample utilities for Glue jobs
# Place your reusable functions here


def init_debugger():
    """
    Initialize debugpy for remote debugging if ENABLE_DEBUG environment variable is set
    """
    import os
    import sys

    if os.environ.get("ENABLE_DEBUG") == "true":
        try:
            print("initializing debugger...")
            import debugpy

            # 5678 is the default attach port in the VS Code debug config
            debugpy.listen(("0.0.0.0", 5678))
            print("⏳ PAUSED: Waiting for debugger to attach on port 5678...")
            print(
                "👉 ACTION REQUIRED: In VS Code, select 'Python: Attach to Glue Job' and press Play (F5) to resume execution."
            )
            debugpy.wait_for_client()
            print("✅ Debugger attached! Resuming execution...")
        except ImportError:
            print("Error: debugpy not installed. Cannot start debugger.")
        except Exception as e:
            print(f"Error starting debugger: {str(e)}")


def clean_column_names(df):
    """
    Clean column names by removing spaces and special characters
    """
    from pyspark.sql.functions import col

    for column in df.columns:
        new_column = column.strip().replace(" ", "_").replace("-", "_").lower()
        if new_column != column:
            df = df.withColumnRenamed(column, new_column)

    return df


def remove_null_columns(df, threshold=0.5):
    """
    Remove columns that have more than threshold (default 50%) null values

    Args:
        df: PySpark DataFrame
        threshold: float between 0 and 1 (percentage of nulls to tolerate)

    Returns:
        DataFrame with columns removed
    """
    total_rows = df.count()
    columns_to_keep = []

    for column in df.columns:
        null_count = df.filter(df[column].isNull()).count()
        null_percentage = null_count / total_rows

        if null_percentage <= threshold:
            columns_to_keep.append(column)
        else:
            print(
                f"Removing column {column} with {null_percentage*100:.2f}% null values"
            )

    return df.select(columns_to_keep)


def get_data_quality_metrics(df):
    """
    Calculate basic data quality metrics for a DataFrame
    """
    metrics = {
        "total_rows": df.count(),
        "total_columns": len(df.columns),
        "column_names": df.columns,
    }

    print(f"\nData Quality Metrics:")
    print(f"Total Rows: {metrics['total_rows']}")
    print(f"Total Columns: {metrics['total_columns']}")
    print(f"Columns: {', '.join(metrics['column_names'])}")

    return metrics
