from bs4 import BeautifulSoup

from src.crawlers.website.page import CrawledPage
from src.crawlers.website.page_queue import PageQueue
from src.crawlers.website.link_extractor import link_extractor
from src.crawlers.website.page_fetcher import page_fetcher


class WebsiteCrawler:
    """
    Crawls a website.
    """

    def crawl(
        self,
        start_url,
        max_pages=10,
        max_depth=2,
    ):

        queue = PageQueue()

        queue.add((start_url, 0))

        visited = set()

        pages = []

        while not queue.empty():

            current_url, depth = queue.get()

            if current_url in visited:
                continue

            if depth > max_depth:
                continue

            visited.add(current_url)

            try:

                response = page_fetcher.fetch(current_url)

                html = response["html"]

                status_code = response["status_code"]

            except Exception as error:

                print(f"✗ Failed to crawl {current_url}")
                print(error)

                continue

            soup = BeautifulSoup(html, "html.parser")

            title = ""

            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            description = ""

            meta = soup.find(
                "meta",
                attrs={"name": "description"},
            )

            if meta:
                description = meta.get(
                    "content",
                    "",
                ).strip()

            canonical_url = ""

            canonical = soup.find(
                "link",
                rel="canonical",
            )

            if canonical:
                canonical_url = canonical.get(
                    "href",
                    "",
                )

            language = ""

            html_tag = soup.find("html")

            if html_tag:
                language = html_tag.get(
                    "lang",
                    "",
                )

            headings = []

            for tag in soup.find_all(
                [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                ]
            ):

                text = tag.get_text(
                    " ",
                    strip=True,
                )

                if text:
                    headings.append(text)

            meta_tags = {}

            for meta in soup.find_all("meta"):

                key = (
                    meta.get("name")
                    or meta.get("property")
                    or meta.get("http-equiv")
                )

                value = meta.get("content")

                if key and value:
                    meta_tags[key] = value

            images = []

            for image in soup.find_all(
                "img",
                src=True,
            ):
                images.append(image["src"])

            navigation_links = []

            page_text = soup.get_text(
                " ",
                strip=True,
            )

            internal_links, external_links = (
                link_extractor.extract(
                    current_url,
                    html,
                )
            )

            page = CrawledPage(
                url=current_url,
                depth=depth,
                title=title,
                description=description,
                canonical_url=canonical_url,
                language=language,
                html=html,
                text=page_text,
                status_code=status_code,
                headings=headings,
                meta_tags=meta_tags,
                navigation_links=navigation_links,
                internal_links=internal_links,
                external_links=external_links,
                images=images,
            )

            pages.append(page)

            if len(pages) >= max_pages:
                break

            for link in internal_links:

                if link not in visited:

                    queue.add(
                        (
                            link,
                            depth + 1,
                        )
                    )

        print(f"✓ Crawled {len(pages)} page(s)")

        return pages


website_crawler = WebsiteCrawler()