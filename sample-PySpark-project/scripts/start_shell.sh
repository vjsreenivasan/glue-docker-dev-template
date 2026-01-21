#!/bin/bash

# Interactive AWS Glue Shell (PySpark)
# Use this for quick testing and debugging

set -e

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_IMAGE="public.ecr.aws/glue/aws-glue-libs:5"

echo "========================================="
echo "Starting AWS Glue PySpark Shell"
echo "========================================="
echo "Workspace: ${WORKSPACE_DIR}"
echo "========================================="
echo ""

docker run -it --rm \
    -v "${WORKSPACE_DIR}:/home/glue_user/workspace/" \
    -e AWS_REGION=ap-southeast-1 \
    -e DISABLE_SSL=true \
    --name glue-shell \
    ${DOCKER_IMAGE} \
    pyspark
