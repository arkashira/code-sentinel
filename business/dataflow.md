# dataflow.md

## System Dataflow Architecture – *Code‑Sentinel*

```
+----------------------+          +----------------------+          +----------------------+
|  External Data       |          |  Ingestion Layer     |          |  Processing/         |
|  Sources (Git, CI/CD |          |  (Kafka / Kinesis)   |          |  Transform Layer     |
|  Repos, Webhooks)    |          |  (Event‑Driven)      |          |  (Spark / Flink)     |
+----------+-----------+          +----------+-----------+          +----------+-----------+
           |                               |                               |
           |                               |                               |
           v                               v                               v
+----------+-----------+          +----------+-----------+          +----------+-----------+
|  Storage Tier (Raw)  |          |  Storage Tier (Processed) |      |  Query/Serving Layer (GraphQL / REST) |
|  (S3 / GCS)          |          |  (PostgreSQL / BigQuery)   |      |  (Auth‑Guarded) |
+----------+-----------+          +----------+-----------+          +----------+-----------+
           |                               |                               |
           |                               |                               |
           v                               v                               v
+----------+-----------+          +----------+-----------+          +----------+-----------+
|  Egress to User      |          |  Egress to User      |          |  Egress to User      |
|  (Dashboard / CLI)   |          |  (API / Webhook)     |          |  (Alert / Report)    |
+----------------------+          +----------------------+          +----------------------+
```

### 1. External Data Sources
| Source | Data Type | Frequency | Auth Boundary |
|--------|-----------|-----------|---------------|
| GitHub / GitLab / Bitbucket | Commit payloads, pull‑request events | Webhook (real‑time) | OAuth 2.0 |
| CI/CD Pipelines (Jenkins, GitHub Actions, GitLab CI) | Build logs, test results | Event stream | API token |
| Code Review Tools (Crucible, Gerrit) | Review comments, diffs | Webhook | OAuth 2.0 |
| Public Vulnerability DBs (NVD, CVE) | CVE metadata | Scheduled pull (daily) | Public API |

### 2. Ingestion Layer
- **Event Bus**: Kafka (or GCP Pub/Sub) for high‑throughput, fault‑tolerant ingestion.
- **Connectors**:  
  - GitHub webhook consumer → Kafka topic `code-events`.  
  - CI/CD webhook consumer → Kafka topic `build-events`.  
  - Scheduled jobs for public DBs → Kafka topic `cve-events`.
- **Schema Registry**: Confluent Schema Registry (Avro) to enforce data contracts.
- **Security**: TLS encryption, IAM roles for producers/consumers, audit logging.

### 3. Processing / Transform Layer
- **Stream Processor**: Apache Flink (or Spark Structured Streaming) consuming Kafka topics.
- **Adversarial Detection Engine**:  
  - ML model (transformer‑based) scoring code snippets for adversarial patterns.  
  - Rule‑based filters (e.g., suspicious imports, obfuscation).  
- **Mitigation Actions**:  
  - Auto‑generation of security comments.  
  - Flagging commits for manual review.  
- **Output**: Structured JSON records to Kafka topic `code-sentinel-events`.

### 4. Storage Tier
| Sub‑Tier | Storage | Use Case | Auth Boundary |
|----------|---------|----------|---------------|
| **Raw** | S3 / GCS (object storage) | Persist raw event payloads for audit & replay | IAM policies, bucket encryption |
| **Processed** | PostgreSQL (or BigQuery) | Store enriched records, detection scores, mitigation actions | Role‑based access control (RBAC) |
| **Analytics** | Snowflake / BigQuery | Long‑term analytics, ML training data | Data‑lake access controls |

### 5. Query / Serving Layer
- **API Gateway**: Kong / API‑Gateway with JWT auth.
- **GraphQL / REST**:  
  - Endpoints: `/commits/{id}`, `/projects/{id}/alerts`, `/reports`.  
  - Pagination, filtering, sorting.  
- **Caching**: Redis for hot queries (e.g., recent alerts).
- **Security**: OAuth 2.0, rate limiting, IP whitelisting.

### 6. Egress to User
| Channel | Interface | Auth Boundary |
|---------|-----------|---------------|
| **Dashboard** | React SPA (Next.js) | OAuth 2.0, SSO |
| **CLI Tool** | `codesentinel-cli` (Python) | API key + TLS |
| **Webhook** | POST to user‑defined URL | HMAC signature |
| **Email / Slack** | Notification service | OAuth 2.0, Slack bot token |

### Auth & Security Summary
- **OAuth 2.0** for all external integrations (GitHub, CI/CD, dashboard).
- **API Keys** for CLI and webhook consumers.
- **TLS** everywhere (in‑transit encryption).
- **IAM** and **RBAC** at storage and API layers.
- **Audit Logging** across ingestion, processing, and serving layers.

---

**Key Metrics to Track**

| Metric | Target | Tool |
|--------|--------|------|
| Event ingestion latency | < 5 s | Kafka metrics |
| Detection accuracy | ≥ 95 % | ML model evaluation |
| Alert false‑positive rate | < 2 % | Post‑processing logs |
| API response time | < 200 ms | Grafana / Prometheus |
| User adoption (active projects) | 100+ | Dashboard analytics |

---