import hashlib

from src.database.repositories.website_snapshot_repository import (
    website_snapshot_repository,
)


class WebsiteSnapshotService:
    """
    Handles website snapshot intelligence.
    """

    def save_snapshot(
        self,
        project,
        website,
    ):

        html_hash = hashlib.sha256(
            website.html.encode("utf-8")
        ).hexdigest()

        latest = website_snapshot_repository.get_latest_snapshot(
            project
        )

        if latest:

            if latest.html_hash == html_hash:

                print("✓ Website unchanged")

                return False

        website_snapshot_repository.add_snapshot(
            project=project,
            url=website.url,
            title=website.title,
            description=website.description,
            html_hash=html_hash,
        )

        print("✓ New website snapshot detected")

        return True

    def get_latest_snapshot(
        self,
        project,
    ):
        """
        Returns the latest saved website snapshot.
        """

        return website_snapshot_repository.get_latest_snapshot(
            project
        )

    def has_changed(
        self,
        project,
        website,
    ):
        """
        Returns True if the website HTML has changed.
        """

        latest = website_snapshot_repository.get_latest_snapshot(
            project
        )

        if latest is None:
            return True

        current_hash = hashlib.sha256(
            website.html.encode("utf-8")
        ).hexdigest()

        return current_hash != latest.html_hash


website_snapshot_service = WebsiteSnapshotService()