from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required
from services.audit_service import AuditService
from storage.json_store import JSONStore
from utils.helpers import get_utc_now_iso, generate_id

testing_bp = Blueprint("testing", __name__, url_prefix="/testing")

def get_testing_store() -> JSONStore:
    return JSONStore(current_app.config["TESTING_DATA_DIR"], "test_runs.json")

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

def seed_default_test_runs(store: JSONStore):
    if store.count() == 0:
        default_runs = [
            {
                "id": generate_id("tr"),
                "name": "Regression Test Suite v1.4",
                "suite_type": "Regression",
                "environment": "Testing",
                "total_tests": 128,
                "passed_tests": 126,
                "failed_tests": 2,
                "skipped_tests": 0,
                "pass_rate": 98.44,
                "status": "PASSED",
                "validation_status": "VALIDATED",
                "executed_by": "qa",
                "created_at": get_utc_now_iso()
            },
            {
                "id": generate_id("tr"),
                "name": "Integration & API Gate Test",
                "suite_type": "Integration",
                "environment": "Staging",
                "total_tests": 64,
                "passed_tests": 64,
                "failed_tests": 0,
                "skipped_tests": 0,
                "pass_rate": 100.0,
                "status": "PASSED",
                "validation_status": "VALIDATED",
                "executed_by": "qa",
                "created_at": get_utc_now_iso()
            },
            {
                "id": generate_id("tr"),
                "name": "Security & Penetration Smoke Test",
                "suite_type": "Security",
                "environment": "Testing",
                "total_tests": 32,
                "passed_tests": 30,
                "failed_tests": 2,
                "skipped_tests": 0,
                "pass_rate": 93.75,
                "status": "FAILED",
                "validation_status": "REJECTED",
                "executed_by": "qa",
                "created_at": get_utc_now_iso()
            }
        ]
        for tr in default_runs:
            store.insert(tr)

@testing_bp.route("/", methods=["GET"])
@login_required
@permission_required("testing.view")
def index():
    store = get_testing_store()
    seed_default_test_runs(store)
    test_runs = store.read_all()

    total_runs = len(test_runs)
    passed_runs = sum(1 for r in test_runs if r.get("status") == "PASSED")
    total_test_cases = sum(r.get("total_tests", 0) for r in test_runs)
    total_passed_cases = sum(r.get("passed_tests", 0) for r in test_runs)
    overall_pass_rate = round((total_passed_cases / total_test_cases * 100), 2) if total_test_cases > 0 else 100.0

    return render_template(
        "testing/index.html",
        test_runs=test_runs,
        total_runs=total_runs,
        passed_runs=passed_runs,
        total_test_cases=total_test_cases,
        overall_pass_rate=overall_pass_rate
    )

@testing_bp.route("/run", methods=["POST"])
@login_required
@permission_required("testing.run")
def run_test_suite():
    name = request.form.get("name", "Automated QA Test Run")
    suite_type = request.form.get("suite_type", "Regression")
    environment = request.form.get("environment", "Testing")

    store = get_testing_store()
    new_run = {
        "id": generate_id("tr"),
        "name": name,
        "suite_type": suite_type,
        "environment": environment,
        "total_tests": 85,
        "passed_tests": 85,
        "failed_tests": 0,
        "skipped_tests": 0,
        "pass_rate": 100.0,
        "status": "PASSED",
        "validation_status": "VALIDATED",
        "executed_by": session.get("username", "QA Engineer"),
        "created_at": get_utc_now_iso()
    }
    store.insert(new_run)

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "QA Engineer"),
        event_type="TEST_SUITE_EXECUTED",
        resource=f"TestSuite:{name}",
        details=f"Executed {suite_type} suite on environment '{environment}' with result PASSED."
    )

    flash(f"Executed test suite '{name}' on {environment} successfully.", "success")
    return redirect(url_for("testing.index"))

@testing_bp.route("/<run_id>/validate", methods=["POST"])
@login_required
@permission_required("testing.validate")
def validate_test_run(run_id: str):
    action = request.form.get("action", "APPROVE")
    store = get_testing_store()
    record = store.find_by_id(run_id)

    if not record:
        flash("Test run record not found.", "danger")
        return redirect(url_for("testing.index"))

    val_status = "VALIDATED" if action == "APPROVE" else "REJECTED"
    record["validation_status"] = val_status
    store.update(run_id, record)

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "QA Engineer"),
        event_type="TEST_VALIDATION_UPDATED",
        resource=f"TestRun:{run_id}",
        details=f"Test run '{record['name']}' validation status updated to '{val_status}'."
    )

    flash(f"Test run '{record['name']}' set to {val_status}.", "info")
    return redirect(url_for("testing.index"))
