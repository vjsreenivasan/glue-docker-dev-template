# AWS Glue Docker Workspace

A complete local development environment for AWS Glue ETL jobs using Docker containers.

## Features

- 🐳 **Docker-based Development**: Run AWS Glue jobs locally using official Glue Docker images
- 🐛 **Remote Debugging**: Attach VS Code debugger to running Glue jobs in containers
- 📓 **Jupyter Notebooks**: Interactive development with Jupyter Lab
- 🔄 **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- ✅ **Code Quality**: Pre-commit hooks with linting, formatting, and security scanning

## Project Structure

```
aws-glue-docker-ws/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline for validation
│       └── deploy.yml       # CD pipeline for AWS deployment
├── sample-PySpark-project/
│   ├── jobs/                # Glue ETL job scripts
│   │   ├── simple_glue_job.py
│   │   └── sample_etl_job.py
│   ├── lib/                 # Shared utilities
│   │   └── glue_utils.py
│   ├── data/
│   │   ├── input/          # Sample input data
│   │   └── output/         # Job output
│   ├── notebooks/          # Jupyter notebooks
│   ├── scripts/
│   │   ├── run_glue_job.sh        # Run jobs in Docker
│   │   ├── debug_wrapper.sh       # Debug helper
│   │   ├── jupyter_wrapper.sh     # Jupyter helper
│   │   └── start_jupyter.sh       # Start Jupyter Lab
│   └── README.md
└── .vscode/
    └── launch.json          # VS Code debug configurations
```

## Quick Start

### Prerequisites

- Docker Desktop installed and running
- VS Code with Python extension
- Git configured

### 1. Clone and Setup

```bash
cd aws-glue-docker-ws
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

### 2. Run a Glue Job

```bash
cd sample-PySpark-project/scripts
./run_glue_job.sh sample_etl_job.py
```

Or use VS Code:
1. Open a job file (e.g., `sample_etl_job.py`)
2. Press **F5**
3. Select **"Run Current Glue Job in Docker"**

### 3. Debug a Glue Job

1. Set breakpoints in your job file
2. Press **F5** → Select **"Run Current Glue Job in Docker (Debug Mode)"**
3. Wait for "Waiting for debugger to attach..."
4. Press **F5** → Select **"Python: Attach to Glue Job"**

### 4. Use Jupyter Notebooks

```bash
cd sample-PySpark-project/scripts
./start_jupyter.sh
```

Then open http://localhost:8888 in your browser.

## Development Workflow

### Local Development

1. **Edit** your Glue job in `sample-PySpark-project/jobs/`
2. **Test locally** using Docker
3. **Debug** with VS Code debugger
4. **Commit** your changes

### CI/CD Pipeline

1. **Push** to feature branch
2. **Create PR** → CI validates code automatically
3. **Merge** → Deploys to AWS dev environment
4. **Manual deploy** to staging/prod via GitHub Actions

See [CI_CD_SETUP.md](CI_CD_SETUP.md) for detailed setup instructions.

## VS Code Launch Configurations

| Configuration | Description |
|--------------|-------------|
| Run Current Glue Job in Docker | Execute job without debugging |
| Run Current Glue Job in Docker (Debug Mode) | Execute with debugger enabled |
| Python: Attach to Glue Job | Attach debugger to running container |
| Start Glue Jupyter Notebook | Launch Jupyter Lab |
| Start Glue PySpark Shell | Interactive PySpark shell |

## Available Scripts

### `run_glue_job.sh`
```bash
./run_glue_job.sh <job_script_name> [--debug]
```

### `start_jupyter.sh`
```bash
./start_jupyter.sh [port]  # Default port: 8888
```

## Environment Variables

Jobs receive these arguments by default:
- `--JOB_NAME`: Name of the job
- `--input_path`: Input data location
- `--output_path`: Output data location

Modify these in `run_glue_job.sh` as needed.

## Sample Jobs

### `simple_glue_job.py`
Basic example demonstrating:
- Reading CSV data
- Simple transformations
- Writing Parquet output

### `sample_etl_job.py`
Advanced example with:
- DynamicFrame operations
- Field mappings
- Partitioned output
- Error handling

## Code Quality Tools

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### Manual Checks
```bash
# Format code
black sample-PySpark-project/jobs/ sample-PySpark-project/lib/

# Lint
flake8 sample-PySpark-project/jobs/ sample-PySpark-project/lib/

# Sort imports
isort sample-PySpark-project/jobs/ sample-PySpark-project/lib/

# Security scan
bandit -r sample-PySpark-project/jobs/ sample-PySpark-project/lib/
```

## Troubleshooting

### Docker Image Not Found
```bash
docker pull amazon/aws-glue-libs:glue_libs_4.0.0_image_01
```

### Permission Denied on Scripts
```bash
chmod +x sample-PySpark-project/scripts/*.sh
```

### Debugger Won't Attach
1. Ensure port 5678 is not in use
2. Check firewall settings
3. Verify the job is waiting (see console logs)

### Jupyter Won't Start
The first run installs JupyterLab - be patient. Check terminal for errors.

## Documentation

- [CI/CD Setup Guide](CI_CD_SETUP.md)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [AWS Glue Docker Images](https://github.com/awslabs/aws-glue-libs)

## Contributing

1. Create a feature branch
2. Make your changes
3. Run pre-commit hooks
4. Create a pull request

## License

This project is for educational and development purposes.

## Support

For issues or questions:
1. Check [CI_CD_SETUP.md](CI_CD_SETUP.md) for setup details
2. Review terminal logs for error messages
3. Check AWS CloudWatch logs for deployed jobs
