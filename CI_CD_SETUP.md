# AWS Glue Docker Workspace - CI/CD Pipeline

This document explains the CI/CD pipeline setup for the AWS Glue project.

## Overview

The project uses **GitHub Actions** for continuous integration and deployment with the following workflows:

### 1. CI Pipeline (`ci.yml`)
Runs on every push and pull request to validate code quality and functionality.

**Jobs:**
- **Lint**: Checks code formatting and style
  - Black formatter validation
  - Flake8 linting
  
- **Validate Jobs**: Tests each Glue job
  - Syntax validation using Python compile
  - Full job execution in Docker
  - Output verification
  
- **Security Scan**: Identifies security vulnerabilities
  - Bandit security analysis
  - Generates security reports

### 2. CD Pipeline (`deploy.yml`)
Deploys validated Glue jobs to AWS environments.

**Features:**
- Deploys to dev/staging/prod environments
- Uploads scripts to S3
- Creates/updates AWS Glue jobs
- Supports manual deployment via workflow_dispatch

**Required Secrets:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`
- `GLUE_EXECUTION_ROLE_ARN`

## Setup Instructions

### 1. Initialize Git Repository

```bash
git config user.email "your-email@example.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repository

```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/aws-glue-docker-ws.git
git branch -M main
git push -u origin main
```

### 3. Configure GitHub Secrets

Go to your repository **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key with Glue permissions | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | `wJalr...` |
| `AWS_ACCOUNT_ID` | Your AWS account ID | `123456789012` |
| `GLUE_EXECUTION_ROLE_ARN` | IAM role for Glue jobs | `arn:aws:iam::123456789012:role/GlueServiceRole` |

### 4. Install Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

This will run automated checks before each commit:
- Code formatting (Black)
- Linting (Flake8)
- Import sorting (isort)
- Security scanning (Bandit)
- Type checking (mypy)

### 5. Create IAM Role for Glue

Your Glue execution role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::glue-scripts-*/*",
        "arn:aws:s3:::glue-scripts-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:/aws-glue/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Workflow Triggers

### CI Workflow
- **Push** to `main` or `develop` branches
- **Pull Request** to `main` or `develop` branches
- **Manual** via GitHub Actions UI

### CD Workflow
- **Push** to `main` branch (auto-deploys to dev)
- **Manual** via GitHub Actions UI (choose environment)

## Local Development

### Run Tests Locally

```bash
# Lint check
black --check sample-PySpark-project/jobs/ sample-PySpark-project/lib/
flake8 sample-PySpark-project/jobs/ sample-PySpark-project/lib/

# Run a specific job
cd sample-PySpark-project/scripts
./run_glue_job.sh sample_etl_job.py
```

### Debug Mode

```bash
# Run with debugger enabled
cd sample-PySpark-project/scripts
./run_glue_job.sh sample_etl_job.py --debug

# In VS Code, attach debugger via "Python: Attach to Glue Job"
```

## Deployment Process

1. **Develop** your Glue jobs locally
2. **Commit** changes to a feature branch
3. **Create PR** to main/develop - CI runs automatically
4. **Merge PR** - CD deploys to dev automatically
5. **Manual Deploy** to staging/prod via GitHub Actions UI

## Monitoring

### GitHub Actions
- View workflow runs in the **Actions** tab
- Check logs for each job
- Download artifacts (security reports)

### AWS CloudWatch
- Glue job logs: `/aws-glue/jobs/`
- Continuous logging enabled
- Job insights enabled

## Troubleshooting

### CI Fails on Lint
```bash
# Auto-fix formatting issues
black sample-PySpark-project/jobs/ sample-PySpark-project/lib/
isort sample-PySpark-project/jobs/ sample-PySpark-project/lib/
git add .
git commit -m "Fix formatting"
```

### Deployment Fails
1. Check AWS credentials are correctly set in GitHub Secrets
2. Verify IAM role has necessary permissions
3. Ensure S3 bucket name is unique globally
4. Check CloudWatch logs for Glue job errors

## Best Practices

1. **Always create feature branches** - don't commit directly to main
2. **Write descriptive commit messages**
3. **Run pre-commit hooks** before pushing
4. **Test locally** before creating PR
5. **Review CI logs** if build fails
6. **Use manual deployment** for production

## Additional Resources

- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pre-commit Hooks](https://pre-commit.com/)
