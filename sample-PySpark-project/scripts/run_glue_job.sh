#!/bin/bash

# Run AWS Glue Job in Docker
# Usage: ./run_glue_job.sh <job_script_name>

set -e

# Configuration
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_IMAGE="public.ecr.aws/glue/aws-glue-libs:5"
JOB_SCRIPT="${1:-simple_glue_job.py}"
JOB_NAME="${2:-local-glue-job}"

# Job parameters (customize as needed)
INPUT_PATH="file:///home/glue_user/workspace/data/input/"
OUTPUT_PATH="file:///home/glue_user/workspace/data/output/"

echo "========================================="
echo "Running AWS Glue Job in Docker"
echo "========================================="
echo "Workspace: ${WORKSPACE_DIR}"
echo "Job Script: ${JOB_SCRIPT}"
echo "Job Name: ${JOB_NAME}"
echo "Input Path: ${INPUT_PATH}"
echo "Output Path: ${OUTPUT_PATH}"
echo "========================================="

# Check if job script exists
if [ ! -f "${WORKSPACE_DIR}/jobs/${JOB_SCRIPT}" ]; then
    echo "Error: Job script not found: ${WORKSPACE_DIR}/jobs/${JOB_SCRIPT}"
    exit 1
fi

# Debug Configuration
DEBUG_PORTS=""
ENV_VARS=""
ENTRYP_CMD="spark-submit"

if [[ "$@" == *"--debug"* ]]; then
    echo "Debug mode enabled"
    DEBUG_PORTS="-p 5678:5678"
    ENV_VARS="-e ENABLE_DEBUG=true"
    # Use the wrapper script to install debugpy inside container
    ENTRYP_CMD="/home/glue_user/workspace/scripts/debug_wrapper.sh"
fi

# Run the Glue job in Docker
docker run -it --rm \
    -v "${WORKSPACE_DIR}:/home/glue_user/workspace/" \
    -e AWS_REGION=us-east-1 \
    -e DISABLE_SSL=true \
    $ENV_VARS \
    $DEBUG_PORTS \
    --name glue-job-runner \
    ${DOCKER_IMAGE} \
    ${ENTRYP_CMD} \
    --py-files /home/glue_user/workspace/lib/ \
    /home/glue_user/workspace/jobs/${JOB_SCRIPT} \
    --JOB_NAME="${JOB_NAME}" \
    --input_path="${INPUT_PATH}" \
    --output_path="${OUTPUT_PATH}"

echo ""
echo "========================================="
echo "Job execution completed!"
echo "========================================="
