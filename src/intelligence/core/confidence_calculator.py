class ConfidenceCalculator:
    """
    Calculates confidence for every signal.
    """

    DEFAULT_CONFIDENCE = 50

    CONFIDENCE = {

        "Website Collector": 100,

        "X Collector": 90,

        "Telegram Collector": 95,

        "Discord Collector": 95,

        "GitHub Collector": 100,

        "Blockchain Collector": 100,
    }

    def calculate(
        self,
        collector,
    ):

        return self.CONFIDENCE.get(
            collector,
            self.DEFAULT_CONFIDENCE,
        )


confidence_calculator = ConfidenceCalculator()