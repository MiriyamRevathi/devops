# DevOpsFlow — Enterprise Local DevOps Control Center

DevOpsFlow is a complete, production-grade local DevOps lifecycle management platform that allows software developers and DevOps engineers to manage the entire application delivery lifecycle locally without any external cloud service or API dependencies.

## Key Features

1. **Interactive DevOps Control Center Dashboard**: Real-time metrics, active projects, pipeline run histories, production deployment status, microservice health cards, and active incident alerts.
2. **Local Authentication & RBAC**: Role-based access control (Admin, DevOps Engineer, Developer, QA Engineer, Viewer) with session handling and password hashing.
3. **Projects Workspace**: Project creation, editing, archiving, team membership, default branch configuration, and search/filtering.
4. **Git Source Control Simulator**: Branch management, commit history, pull request creation, peer code review, and non-fast-forward merge workflows.
5. **Interactive CI Pipeline Engine**: Stage builder (Checkout, Install, Lint, Validate, Unit Test, Integration Test, Build, Package, Security Scan, Publish Artifact), status state machine (CREATED ➔ QUEUED ➔ RUNNING ➔ SUCCESS / FAILED), and live log stream output.
6. **CD & Multi-Environment Deployment System**: Target environments (Development, Testing, Staging, Production), deployment approvals, release versioning, and automated rollbacks.
7. **Release Management**: Tagged release versions, changelog notes, artifact manifests, and deployment targets.
8. **Microservice Catalog**: Service discovery, CPU/RAM/Request telemetry, health diagnostics, dependency graph, and restart simulation.
9. **Safe Container Engine Simulator**: Start, stop, restart, inspect, and remove simulated containers with port bindings and resource tracking without requiring local Docker daemon.
10. **Infrastructure-as-Code (IaC) Engine**: Terraform-style `PLAN ➔ REVIEW ➔ APPLY ➔ DESTROY` workflow with YAML syntax parser and resource state tracker.
11. **System Monitoring & Telemetry**: Telemetry metrics collection via `psutil`, `numpy`, and `pandas`.
12. **DORA 4 Key DevOps Metrics**: Automated calculation of Deployment Frequency, Lead Time for Changes, Change Failure Rate (CFR), and Mean Time to Recovery (MTTR) with performance ratings.
13. **Centralized Log Viewer**: Structured log aggregator with multi-level severity filtering (`INFO`, `WARNING`, `ERROR`, `DEBUG`) and trace ID tracking.
14. **Incident Management & SLA Tracker**: Incident filing, severity levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), status workflows (`OPEN` ➔ `INVESTIGATING` ➔ `MITIGATING` ➔ `RESOLVED` ➔ `CLOSED`), and timeline events.
15. **Automated Alert Rules**: Threshold-based alert rules engine (`CPU > 80%`, `Memory > 85%`, `Error Rate > 5%`).
16. **Local Security Dashboard**: Dependency scanner, misconfiguration audit, and secret leak pattern detection.
17. **Artifact Registry**: Local package store for wheels, tars, zips, and container image metadata.
18. **Engineering Teams & RBAC**: Team management and user role assignments.
19. **DevOps Task Kanban Board**: Task cards organized in `Backlog`, `Ready`, `In Progress`, `Review`, and `Done` columns with status movement.
20. **Change Request Management (CAB)**: Managed change advisory board workflow (`DRAFT` ➔ `SUBMITTED` ➔ `REVIEW` ➔ `APPROVED` ➔ `IMPLEMENTING` ➔ `VERIFIED` ➔ `CLOSED`) with risk & impact evaluation.
21. **Immutable Audit Trail Registry**: Searchable system audit event history tracking every login, pipeline execution, deployment, and infrastructure change.

---

## Architecture & Technology Stack

- **Backend**: Python 3.10+, Flask Application Factory, Werkzeug, Jinja2, pandas, numpy, matplotlib, psutil, PyYAML.
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (responsive design, no external Node.js/React dependencies).
- **Persistence**: Thread-safe file-based JSON storage engines with locking and index search.
- **Testing**: pytest unit and integration test suite.

---

## Local Installation & Quick Start

1. **Clone or Navigate to Project Directory**:
   ```bash
   cd C:\Users\miriy\.gemini\antigravity\scratch\devopsflow
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**:
   ```bash
   python app.py
   ```

4. **Access Platform**:
   Open browser at: `http://127.0.0.1:5000`

---

## Demo User Credentials

| Username | Password | Role |
| :--- | :--- | :--- |
| `admin` | `admin123` | Admin |
| `devops` | `devops123` | DevOps Engineer |
| `developer` | `dev123` | Developer |
| `qa` | `qa123` | QA Engineer |
| `viewer` | `viewer123` | Viewer |

---

## Running Automated Tests

Run full test suite with `pytest`:
```bash
pytest
```

---

## Docker Deployment

Build and run via Docker:
```bash
docker build -t devopsflow .
docker run -p 5000:5000 devopsflow
```
