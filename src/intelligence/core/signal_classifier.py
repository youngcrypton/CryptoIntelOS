class SignalClassifier:
    """
    Determines the category of a signal.
    """

    CATEGORIES = {

        "Website": "Infrastructure",

        "X Profile": "Social",

        "Telegram": "Community",

        "Discord": "Community",

        "GitHub": "Development",

        "Tokenomics": "Economics",

        "Governance": "Governance",

        "Treasury": "Finance",
    }

    def classify(
        self,
        signal_type,
    ):

        return self.CATEGORIES.get(
            signal_type,
            "General",
        )


signal_classifier = SignalClassifier()