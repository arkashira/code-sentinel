# Tech Spec: Code Sentinel
=====================================

## Stack
---------------

*   **Language**: Python 3.9+
*   **Framework**: FastAPI
*   **Runtime**: Docker (with multi-stage build)
*   **Database**: PostgreSQL 13+ (with Docker)
*   **Storage**: Redis 7+ (with Docker)

## Hosting
------------

*   **Free-tier-first**: Heroku Free Tier
*   **Specific platforms**: AWS Elastic Beanstalk (with Docker), Google Cloud Run (with Docker)

## Data Model
--------------

### Tables/Collections

*   **adversarial_code**: stores detected adversarial AI-generated code
	+   **id** (primary key): UUID
	+   **code**: string (detected code)
	+   **timestamp**: timestamp (when detected)
*   **mitigation_strategies**: stores applied mitigation strategies
	+   **id** (primary key): UUID
	+   **strategy**: string (applied strategy)
	+   **timestamp**: timestamp (when applied)
*   **project_metadata**: stores project metadata
	+   **id** (primary key): UUID
	+   **project_name**: string (project name)
	+   **project_description**: string (project description)

## API Surface
----------------

### Endpoints

*   **POST /detect**: detects adversarial AI-generated code in a given code snippet
	+   **Request Body**: JSON object with `code` field (string)
	+   **Response**: JSON object with `detected` field (boolean) and `adversarial_code` field (string)
*   **POST /mitigate**: applies mitigation strategies to detected adversarial AI-generated code
	+   **Request Body**: JSON object with `code` field (string) and `strategy` field (string)
	+   **Response**: JSON object with `mitigated` field (boolean) and `mitigation_strategy` field (string)
*   **GET /project-metadata**: retrieves project metadata
	+   **Response**: JSON object with `project_name` field (string) and `project_description` field (string)
*   **POST /project-metadata**: creates or updates project metadata
	+   **Request Body**: JSON object with `project_name` field (string) and `project_description` field (string)
	+   **Response**: JSON object with `project_name` field (string) and `project_description` field (string)
*   **DELETE /project-metadata**: deletes project metadata
	+   **Response**: JSON object with `success` field (boolean)

## Security Model
-----------------

*   **Authentication**: OAuth 2.0 with JWT tokens
*   **Authorization**: IAM roles with fine-grained permissions
*   **Secrets**: stored in HashiCorp Vault
*   **Encryption**: data at rest encrypted with AES-256

## Observability
----------------

*   **Logs**: stored in ELK Stack (Elasticsearch, Logstash, Kibana)
*   **Metrics**: collected with Prometheus and Grafana
*   **Traces**: collected with Jaeger

## Build/CI
------------

*   **Build**: multi-stage Docker build with GitHub Actions
*   **CI**: GitHub Actions with automated testing and deployment
*   **CD**: automated deployment to Heroku Free Tier and AWS Elastic Beanstalk