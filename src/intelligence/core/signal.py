from dataclasses import dataclass


@dataclass
class Signal:
    """
    Represents one intelligence signal generated
    anywhere inside CryptoIntel OS.
    """

    project: str

    source: str

    signal_type: str

    category: str

    severity: str

    confidence: int

    score: int

    title: str

    summary: str

    evidence: str