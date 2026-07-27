from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


class LinkExtractor:
    """
    Extracts links from HTML.
    """

    def extract(
        self,
        base_url,
        html,
    ):

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        internal = []

        external = []

        base_domain = urlparse(base_url).netloc

        for link in soup.find_all(
            "a",
            href=True,
        ):

            href = urljoin(
                base_url,
                link["href"],
            )

            domain = urlparse(href).netloc

            if domain == base_domain:

                internal.append(href)

            else:

                external.append(href)

        return internal, external


link_extractor = LinkExtractor()