import warnings


class Scheduler:
    """
    Placeholder scheduler.

    Later this will support:

    • Cron
    • Fixed intervals
    • Event-driven execution
    """

    def run(self):

        warnings.warn(
            "src.orchestrator.scheduler is obsolete; scheduling must invoke Platform SDK",
            DeprecationWarning,
            stacklevel=2,
        )

        print(
            "[Scheduler] Ready."
        )


scheduler = Scheduler()
