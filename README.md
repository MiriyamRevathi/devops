# DevOpsFlow — Enterprise DevOps Control Center & RBAC Platform

DevOpsFlow is a production-grade enterprise DevOps Control Center featuring a granular, function-based Role-Based Access Control (RBAC) authorization engine, multi-environment continuous deployment orchestrator, local container simulator, infrastructure-as-code planner, DORA metrics calculator, and centralized audit logging.

---

## 🔒 Role-Based Access Control (RBAC) System

DevOpsFlow defines 45+ granular permissions enforced strictly at the backend route level.

### Demo User Accounts

| Role | Username | Password | Access & Responsibilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full system access. Manages users, roles, teams, global settings, deployments, infrastructure, audit logs. |
| **DevOps Engineer** | `devops` | `devops123` | Operational lead. Manages CI/CD pipelines, deployments, releases, infrastructure (plan/apply/destroy), containers, incidents, security scans. |
| **Developer** | `developer` | `dev123` | Development engineer. Manages projects, branches, commits, PRs, dev builds, incidents. (Restricted from Production deployments & Infra apply). |
| **QA Engineer** | `qa` | `qa123` | Quality lead. Dedicated Testing Dashboard (`/testing`), regression runs, PR reviews, testing/staging validation, defect management. (Restricted from Production deployments). |
| **Viewer** | `viewer` | `viewer123` | Completely read-only across all dashboards, metrics, logs, deployments, and resources. (All mutations restricted). |

---

## 🚀 Deterministic Local Installation & Run Commands

### Prerequisites
- Python 3.10+
- Git

### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/MiriyamRevathi/devops.git
cd devops

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run test suite
pytest

# 4. Start local platform server
python app.py
```

The application will launch on **http://127.0.0.1:5007**.

---

## 🛠️ Security & Safety Rules Enforced
- **Production Protection**: Production deployments and production rollbacks are strictly restricted to `Admin` and `DevOps Engineer` roles.
- **Admin Safety Rules**: The system prevents deleting or demoting the last active `Admin` account or self-demoting the logged-in admin.
- **Backend Route Enforcement**: Accessing restricted URLs directly returns a HTTP 403 Forbidden page.
- **Icon-Free Design System**: Clean typography, status badges, data tables, and modal dialogs with zero decorative icons or emojis.
- **Audit Logging**: Every mutation event is recorded in the system audit trail.
