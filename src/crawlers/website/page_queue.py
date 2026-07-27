from collections import deque


class PageQueue:
    """
    FIFO queue used by the website crawler.

    Each item stored is:

        (
            url,
            depth,
        )
    """

    def __init__(self):

        self._queue = deque()

        self._seen = set()

    def add(
        self,
        item,
    ):

        url, depth = item

        if url in self._seen:

            return

        self._seen.add(url)

        self._queue.append(item)

    def get(self):

        return self._queue.popleft()

    def empty(self):

        return len(self._queue) == 0

    def size(self):

        return len(self._queue)

    def clear(self):

        self._queue.clear()

        self._seen.clear()