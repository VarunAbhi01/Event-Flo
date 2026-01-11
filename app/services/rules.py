from dataclasses import dataclass
from typing import Dict, Any

from app.db.models import SeverityLevel

# dataclass is only to hold data structure.
# if we wanted to insert data into a normal class during runtime we would have to write init method to initialize the variables but with dataclass we can avoid that boilerplate code like the below:
# class Result:
    # def __init__(self, severity, reason, recommendation, escalate):
    #     self.severity = severity
    #     self.reason = reason
    #     self.recommendation = recommendation
    #     self.escalate = escalate
# instead of this we can simply use dataclass like below calssification result and simply call it with data insertion into it.


@dataclass
# define what the classification result class will look like
class ClassificationResult:
    severity: SeverityLevel
    classification_reason: str
    recommendation: str
    should_escalate: bool


def classify_event(event_type: str, payload: Dict[str, Any]) -> ClassificationResult:
    """
    Applies business rules to classify an event.
    """

    if event_type == "payment_failed":
        amount = payload.get("amount", 0)

        if amount >= 1000:
            return ClassificationResult(
                severity=SeverityLevel.critical,
                classification_reason="Payment amount is greater than or equal to 1000",
                recommendation="Escalate to finance team immediately",
                should_escalate=True
            )
        else:
            return ClassificationResult(
                severity=SeverityLevel.high,
                classification_reason="Payment failed but amount is below critical threshold",
                recommendation="Notify customer and retry payment",
                should_escalate=False
            )

    elif event_type == "sla_breach":
        minutes_over = payload.get("minutes_over", 0)

        if minutes_over >= 30:
            return ClassificationResult(
                severity=SeverityLevel.high,
                classification_reason="SLA breached by more than 30 minutes",
                recommendation="Alert operations team",
                should_escalate=True
            )
        else:
            return ClassificationResult(
                severity=SeverityLevel.warning,
                classification_reason="Minor SLA breach",
                recommendation="Log incident and monitor",
                should_escalate=False
            )

    elif event_type == "system_error":
        return ClassificationResult(
            severity=SeverityLevel.critical,
            classification_reason="System error detected",
            recommendation="Investigate system logs immediately",
            should_escalate=True
        )

    else:
        return ClassificationResult(
            severity=SeverityLevel.low,
            classification_reason="Unknown event type",
            recommendation="No action required",
            should_escalate=False
        )