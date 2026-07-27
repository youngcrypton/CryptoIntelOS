class BaseRule:
    """
    Base class for every intelligence rule.
    """

    name = "Base Rule"

    def applies_to(
        self,
        signal,
        previous,
        current,
    ):
        """
        Returns True if this rule should run.
        """

        raise NotImplementedError

    def evaluate(
        self,
        signal,
        previous,
        current,
    ):
        """
        Returns either None or a new intelligence finding.
        """

        raise NotImplementedError