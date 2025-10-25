# Dagster Deployment Infrastructure

This repository contains the infrastructure setup for Dagster deployment with Docker Compose. The workspace has been completely removed and the system is ready for external job deployment.

## Current Status

- **Workspace Removed**: All workspace directories and project files have been completely removed
- **Infrastructure Ready**: Dagster infrastructure is fully configured and running
- **Environment Variables**: All configuration is externalized via environment variables
- **Empty Workspace**: Ready to receive job definitions from external repositories

## Architecture

### Services
- **PostgreSQL**: Database for Dagster storage (run storage, schedule storage, event log storage)
- **Dagster Webserver**: Web UI accessible at http://localhost:3000
- **Dagster Daemon**: Background process for running jobs, schedules, and sensors

### Workspace
- **Empty Workspace**: No projects currently configured
- **Ready for Deployment**: Can receive job definitions from external repositories

## Quick Start

1. **Copy environment file**: `cp env.example .env`
2. **Update configuration**: Edit `.env` with your values
3. **Start services**: `docker compose up -d --build`
4. **Access UI**: Visit http://localhost:3000

## Environment Variables

All configuration is managed via environment variables in `.env`:

- **Database**: `POSTGRES_*`, `DAGSTER_POSTGRES_*`
- **Docker**: `DOCKER_NETWORK_NAME`, `DOCKER_WEBSERVER_PORT`, `DOCKER_WEBSERVER_HOST`
- **Storage**: `IO_MANAGER_STORAGE_PATH`
- **Security**: `DAGSTER_TELEMETRY_ENABLED`

## Adding Jobs

To add jobs to this deployment:

1. **Create job definitions** in external repositories
2. **Add projects** to `workspace.yaml` with appropriate configuration
3. **Deploy jobs** by updating the workspace configuration
4. **Restart containers** to pick up new job definitions

## Project Structure

```
├── dagster_home/
│   └── dagster.yaml          # Dagster configuration
├── workspace.yaml            # Empty workspace configuration
├── docker-compose.yml        # Docker services definition
├── Dockerfile.dagster        # Dagster container definition
├── env.example               # Environment variables template
└── requirements.txt          # Python dependencies
```

## Commands

- **Start**: `docker compose up -d --build`
- **Stop**: `docker compose down`
- **Logs**: `docker compose logs -f`
- **Status**: `docker compose ps`