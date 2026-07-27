class SignalScore:
    """
    Calculates how important a signal is.
    """

    DEFAULT_SCORE = 50

    SCORES = {

        "Website": 60,

        "X Profile": 40,

        "Telegram": 70,

        "Discord": 70,

        "GitHub": 85,

        "Tokenomics": 95,

        "Governance": 90,

        "Treasury": 100,
    }

    def calculate(
        self,
        signal_type,
    ):

        return self.SCORES.get(
            signal_type,
            self.DEFAULT_SCORE,
        )


signal_score = SignalScore()