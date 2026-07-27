from src.intelligence.normalizers.base_normalizer import (
    BaseNormalizer,
)


class XNormalizer(BaseNormalizer):
    """
    Converts X profiles into a normalized structure.
    """

    def normalize(self, profile):

        return {
            "username": profile.username,
            "display_name": profile.display_name,
            "followers": profile.followers,
            "following": profile.following,
            "verified": profile.verified,
            "bio": profile.bio,
        }


x_normalizer = XNormalizer()