#!/bin/bash
set -e

# Debug wrapper for Glue jobs
# Installs debug tools if needed before running spark-submit

if [ "$ENABLE_DEBUG" = "true" ]; then
    echo "========================================="
    echo "Initializing Debug Environment"
    echo "========================================="
    echo "Installing debugpy..."
    pip install debugpy
    echo "Debugpy installed."
fi

echo "Starting Spark Submit..."
exec spark-submit "$@"
