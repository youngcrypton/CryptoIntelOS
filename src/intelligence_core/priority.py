"""Priority helpers for shared intelligence signals."""

from .enums import MonitoringPriority, SignalSeverity


def priority_for_severity(severity: SignalSeverity) -> MonitoringPriority:
    """Map signal severity to a sensible default monitoring priority."""

    mapping = {
        SignalSeverity.INFO: MonitoringPriority.LOW,
        SignalSeverity.LOW: MonitoringPriority.LOW,
        SignalSeverity.MEDIUM: MonitoringPriority.MEDIUM,
        SignalSeverity.HIGH: MonitoringPriority.HIGH,
        SignalSeverity.CRITICAL: MonitoringPriority.CRITICAL,
    }
    return mapping[severity]
