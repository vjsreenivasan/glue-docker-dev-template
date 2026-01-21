#!/bin/bash
set -e

echo "Installing JupyterLab..."
export PATH=$PATH:/home/hadoop/.local/bin
pip3 install jupyterlab --quiet

echo "Starting JupyterLab..."
# Run jupyter lab directly since we updated the PATH
jupyter-lab --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --notebook-dir=/home/glue_user/workspace/
