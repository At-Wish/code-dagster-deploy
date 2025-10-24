# Dagster Docker Deployment

Simple Dagster deployment with Docker Compose. Includes Dagster Daemon, PostgreSQL, and example projects.

## What's Included

- **Dagster Daemon**: Runs jobs and schedules
- **PostgreSQL**: Stores metadata and run history
- **Example Projects**: ETL, Analytics, and ML pipelines

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp env.example .env

# Edit if needed (defaults work fine)
nano .env
```

### 2. Start Services

```bash
# Build and start all services
docker compose up -d

# Check status
docker compose ps
```

### 3. Verify Setup

```bash
# Check logs
docker compose logs dagster-daemon

# Check database
docker compose exec postgres pg_isready -U dagster -d dagster
```

## Project Structure

```
├── docker-compose.yml          # Main services
├── Dockerfile.dagster         # Dagster container
├── requirements.txt           # Python dependencies
├── env.example               # Environment template
├── dagster_home/             # Dagster configuration
│   └── dagster.yaml         # Main config
└── workspace/               # Your projects
    ├── workspace.yaml       # Project registry
    ├── project_a/           # ETL Pipeline
    ├── project_b/           # Analytics
    └── project_c/           # ML Pipeline
```

## Managing Jobs

### List Available Jobs

```bash
docker compose exec dagster-daemon dagster job list
```

### Run a Job

```bash
# Run ETL pipeline
docker compose exec dagster-daemon dagster job execute --job etl_pipeline

# Run analytics pipeline
docker compose exec dagster-daemon dagster job execute --job analytics_pipeline

# Run ML pipeline
docker compose exec dagster-daemon dagster job execute --job ml_pipeline
```

### Check Run History

```bash
# List all runs
docker compose exec dagster-daemon dagster run list

# Get run details
docker compose exec dagster-daemon dagster run show <run-id>
```

## Adding Projects from Different Repositories

If your Dagster projects are in separate Git repositories, you have several options:

### Option 1: Git Submodules (Recommended)

```bash
# Add your project repositories as submodules
git submodule add https://github.com/your-org/etl-project.git workspace/etl-project
git submodule add https://github.com/your-org/analytics-project.git workspace/analytics-project
git submodule add https://github.com/your-org/ml-project.git workspace/ml-project

# Update workspace.yaml to point to submodule projects
```

Update `workspace/workspace.yaml`:

```yaml
load_from:
  - python_file:
      relative_path: etl-project/repo.py
      working_directory: workspace/etl-project
  - python_file:
      relative_path: analytics-project/repo.py
      working_directory: workspace/analytics-project
  - python_file:
      relative_path: ml-project/repo.py
      working_directory: workspace/ml-project
```

### Option 2: Clone Repositories Directly

```bash
# Clone repositories into workspace
cd workspace
git clone https://github.com/your-org/etl-project.git
git clone https://github.com/your-org/analytics-project.git
git clone https://github.com/your-org/ml-project.git
```

### Option 3: Mount External Directories

Modify `docker-compose.yml` to mount external project directories:

```yaml
services:
  dagster-daemon:
    # ... existing configuration
    volumes:
      - ./dagster_home:/opt/dagster/dagster_home
      - ./workspace:/opt/dagster/workspace
      - /path/to/external/etl-project:/opt/dagster/workspace/etl-project
      - /path/to/external/analytics-project:/opt/dagster/workspace/analytics-project
```

### Option 4: Use Git URLs in Workspace

You can also reference projects directly from Git URLs:

```yaml
load_from:
  - python_file:
      relative_path: repo.py
      working_directory: workspace/etl-project
      executable_path: python
  - python_file:
      relative_path: repo.py
      working_directory: workspace/analytics-project
      executable_path: python
```

### Managing Multiple Repositories

#### Updating Projects

```bash
# If using submodules
git submodule update --remote

# If using direct clones
cd workspace/etl-project && git pull
cd workspace/analytics-project && git pull
```

#### Project Dependencies

Each project can have its own `requirements.txt`:

```bash
# workspace/etl-project/requirements.txt
dagster==1.6.8
pandas==2.1.4
sqlalchemy==2.0.25

# workspace/analytics-project/requirements.txt
dagster==1.6.8
matplotlib==3.8.2
plotly==5.17.0
```

Update main `requirements.txt` to include all project dependencies, or modify `Dockerfile.dagster` to install project-specific requirements.

#### Environment Variables per Project

Projects can use different environment variables:

```yaml
# workspace/workspace.yaml
load_from:
  - python_file:
      relative_path: repo.py
      working_directory: workspace/etl-project
      executable_path: python
      env_vars:
        PROJECT_NAME: etl
        DATABASE_URL: postgresql://user:pass@host/db1
  - python_file:
      relative_path: repo.py
      working_directory: workspace/analytics-project
      executable_path: python
      env_vars:
        PROJECT_NAME: analytics
        DATABASE_URL: postgresql://user:pass@host/db2
```

### Best Practices for Multi-Repository Setup

1. **Consistent Structure**: Ensure all project repositories have the same structure
2. **Version Pinning**: Pin Dagster versions across all projects
3. **Shared Dependencies**: Use a shared base requirements file
4. **Environment Management**: Use consistent environment variable naming
5. **Documentation**: Document each project's specific requirements

### Example Multi-Repository Structure

```
code-dagster-deploy/
├── docker-compose.yml
├── requirements.txt              # Shared dependencies
├── dagster_home/
│   └── dagster.yaml
└── workspace/
    ├── workspace.yaml           # References all projects
    ├── etl-project/             # Git submodule or clone
    │   ├── repo.py
    │   └── requirements.txt
    ├── analytics-project/       # Git submodule or clone
    │   ├── repo.py
    │   └── requirements.txt
    └── ml-project/             # Git submodule or clone
        ├── repo.py
        └── requirements.txt
```

## Adding New Projects

### 1. Create Project Directory

```bash
mkdir workspace/my_project
```

### 2. Create Dagster Code

```python
# workspace/my_project/repo.py
from dagster import Definitions, job, op

@op
def my_op():
    return "Hello World!"

@job
def my_job():
    my_op()

defs = Definitions(jobs=[my_job])
```

### 3. Register Project

```yaml
# workspace/workspace.yaml
load_from:
  - python_file:
      relative_path: my_project/repo.py
      working_directory: workspace/my_project
```

### 4. Restart Services

```bash
docker compose restart dagster-daemon
```

## Common Operations

### Start Services

```bash
docker compose up -d
```

### Stop Services

```bash
docker compose down
```

### Restart Services

```bash
docker compose restart
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f dagster-daemon
docker compose logs -f postgres
```

### Database Operations

```bash
# Connect to database
docker compose exec postgres psql -U dagster -d dagster

# Backup database
docker compose exec postgres pg_dump -U dagster -d dagster > backup.sql

# Restore database
docker compose exec -T postgres psql -U dagster -d dagster < backup.sql
```

## Example Projects

### Project A: ETL Pipeline
- **Jobs**: `etl_pipeline`
- **Assets**: `daily_summary`
- **Schedule**: Daily at 2 AM
- **Purpose**: Data extraction, transformation, and loading

### Project B: Analytics
- **Jobs**: `analytics_pipeline`
- **Assets**: `dashboard_data`
- **Schedule**: Daily at 6 AM
- **Purpose**: Business metrics and reporting

### Project C: ML Pipeline
- **Jobs**: `ml_pipeline`
- **Assets**: `model_performance_metrics`
- **Sensors**: `data_drift_sensor`
- **Purpose**: Machine learning model training and deployment

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Database passwords
POSTGRES_PASSWORD=your_password
DAGSTER_POSTGRES_PASSWORD=your_password

# Dagster settings
DAGSTER_HOME=/opt/dagster/dagster_home
DAGSTER_CURRENT_IMAGE=dagster-daemon:latest
DAGSTER_TELEMETRY_ENABLED=false
```

### Dagster Configuration

Edit `dagster_home/dagster.yaml`:

```yaml
storage:
  postgres:
    postgres_db:
      hostname: postgres
      db_name: dagster
      username: dagster
      password: ${DAGSTER_POSTGRES_PASSWORD}
      port: 5432

run_coordinator:
  module: dagster.core.run_coordinator
  class: QueuedRunCoordinator
  config:
    max_concurrent_runs: 5

scheduler:
  module: dagster.core.scheduler
  class: DagsterDaemonScheduler
```
