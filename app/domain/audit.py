from datetime import datetime, timezone
import uuid

def create_audit_record(customer_id,risk_result):
    # Create a traceable record for one borrower risk calcuation
    return{
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "customer_id": customer_id,
        "default_probability": risk_result["default_probability"],
        "risk_band": risk_result["risk_band"]
    }
