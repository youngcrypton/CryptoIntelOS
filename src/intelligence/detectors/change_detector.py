class ChangeDetector:
    """
    Compares two normalized dictionaries and returns
    every detected change.
    """

    def compare(
        self,
        previous,
        current,
    ):

        changes = []

        if previous is None:

            return changes

        all_fields = set(previous.keys()) | set(current.keys())

        for field in sorted(all_fields):

            old_value = previous.get(field)
            new_value = current.get(field)

            if old_value != new_value:

                changes.append(
                    {
                        "field": field,
                        "old": old_value,
                        "new": new_value,
                    }
                )

        return changes


change_detector = ChangeDetector()