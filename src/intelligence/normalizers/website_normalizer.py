import hashlib

from src.intelligence.normalizers.base_normalizer import (
    BaseNormalizer,
)


class WebsiteNormalizer(BaseNormalizer):
    """
    Converts website snapshots into a normalized structure
    that can be used by the intelligence engine.
    """

    def normalize(self, website):

        return {

            # ----------------------------------
            # Basic Information
            # ----------------------------------

            "url": website.url,

            "title": website.title,

            "description": website.description,

            "html_hash": hashlib.sha256(
                website.html.encode("utf-8")
            ).hexdigest(),

            # ----------------------------------
            # SEO
            # ----------------------------------

            "canonical_url": website.canonical_url,

            "language": website.language,

            # ----------------------------------
            # Structured Content
            # ----------------------------------

            "headings": website.headings,

            "meta_tags": website.meta_tags,

            # ----------------------------------
            # Links
            # ----------------------------------

            "navigation_links": website.navigation_links,

            "internal_links": website.internal_links,

            "external_links": website.external_links,

            # ----------------------------------
            # Media
            # ----------------------------------

            "images": website.images,

            # ----------------------------------
            # Intelligence
            # ----------------------------------

            "page_text": website.page_text,

            "keywords": website.keywords,
        }


website_normalizer = WebsiteNormalizer()