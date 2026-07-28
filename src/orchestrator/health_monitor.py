class HealthMonitor:
    """
    Tracks collector health.
    """

    def __init__(self):

        self.status = {}

    def healthy(self, collector):

        self.status[collector] = "Healthy"

    def failed(self, collector):

        self.status[collector] = "Failed"

    def report(self):

        return self.status


health_monitor = HealthMonitor()