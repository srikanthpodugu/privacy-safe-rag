import json
import os
from datetime import datetime


class AuditLogger:

    def __init__(self):

        self.log_file = "audit_logs.json"

        # Create file if not exists
        if not os.path.exists(self.log_file):

            with open(self.log_file, "w") as f:
                json.dump([], f)

    # ==========================================================
    # WRITE AUDIT EVENT
    # ==========================================================
    def log_event(
        self,
        filename,
        domain,
        risk_score,
        risk_level,
        governance_action,
        entity_breakdown
    ):

        event = {

            "timestamp": datetime.utcnow().isoformat(),

            "filename": filename,

            "domain": domain,

            "risk_score": risk_score,

            "risk_level": risk_level,

            "governance_action": governance_action,

            "entity_breakdown": entity_breakdown
        }

        # Read existing logs
        with open(self.log_file, "r") as f:

            logs = json.load(f)

        logs.append(event)

        # Save updated logs
        with open(self.log_file, "w") as f:

            json.dump(logs, f, indent=2)
