from src.database.repositories.x_profile_repository import (
    x_profile_repository,
)


class XProfileSnapshotService:
    """
    Handles X profile snapshots and detects profile changes.
    """

    def save_snapshot(self, project, profile):
        """
        Save a profile snapshot if it changed.
        """

        latest = x_profile_repository.get_latest_snapshot(project)

        if latest:

            if (
                latest.username == profile.username
                and latest.display_name == profile.display_name
                and latest.bio == profile.bio
                and latest.followers == profile.followers
                and latest.following == profile.following
                and latest.verified == profile.verified
                and latest.website == profile.website
                and latest.joined == profile.joined
                and latest.profile_image == profile.profile_image
                and latest.banner_image == profile.banner_image
            ):
                print("✓ X profile unchanged")
                return False

        x_profile_repository.add_snapshot(
            project=project,
            username=profile.username,
            display_name=profile.display_name,
            bio=profile.bio,
            followers=profile.followers,
            following=profile.following,
            verified=profile.verified,
            website=profile.website,
            joined=profile.joined,
            profile_image=profile.profile_image,
            banner_image=profile.banner_image,
        )

        print("✓ New X profile snapshot detected")

        return True


x_profile_snapshot_service = XProfileSnapshotService()