"""Canonical module entry point for ``python -m src`` and Docker."""


def main() -> None:
    """Load application dependencies only when startup is requested."""

    from src.core.app import run

    run()


if __name__ == "__main__":
    main()
