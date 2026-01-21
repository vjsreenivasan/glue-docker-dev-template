#!/bin/bash

# Start AWS Glue Jupyter Notebook in Docker
# This allows you to develop and test Glue jobs interactively

set -e

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_IMAGE="public.ecr.aws/glue/aws-glue-libs:5"
JUPYTER_PORT="${1:-8888}"

echo "========================================="
echo "Starting AWS Glue Jupyter Notebook"
echo "========================================="
echo "Workspace: ${WORKSPACE_DIR}"
echo "Jupyter Port: ${JUPYTER_PORT}"
echo "========================================="
echo ""
echo "Access Jupyter Notebook at: http://localhost:${JUPYTER_PORT}"
echo "Token will be displayed below..."
echo ""

docker run -it --rm \
    -v "${WORKSPACE_DIR}:/home/glue_user/workspace/" \
    -e AWS_REGION=us-east-1 \
    -e DISABLE_SSL=true \
    -p ${JUPYTER_PORT}:8888 \
    -p 4040:4040 \
    --name glue-jupyter \
    ${DOCKER_IMAGE} \
    /home/glue_user/workspace/scripts/jupyter_wrapper.sh
