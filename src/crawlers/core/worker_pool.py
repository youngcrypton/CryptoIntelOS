from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class WorkerPool:
    """
    Executes tasks concurrently using worker threads.
    """

    def __init__(self, max_workers=5):

        self.max_workers = max_workers

    def run(self, function, items):

        results = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = {
                executor.submit(function, item): item
                for item in items
            }

            for future in as_completed(futures):

                try:

                    result = future.result()

                    if result is not None:

                        results.append(result)

                except Exception as error:

                    print(
                        f"Worker Error: {error}"
                    )

        return results


worker_pool = WorkerPool()