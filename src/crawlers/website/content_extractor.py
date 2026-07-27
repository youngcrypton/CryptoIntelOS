class ContentExtractor:
    """
    Extracts structured information from HTML.
    """

    def extract_title(
        self,
        soup,
    ):

        if soup.title and soup.title.string:

            return soup.title.string.strip()

        return ""

    def extract_description(
        self,
        soup,
    ):

        meta = soup.find(
            "meta",
            attrs={
                "name": "description",
            },
        )

        if meta:

            return meta.get(
                "content",
                "",
            ).strip()

        return ""

    def extract_language(
        self,
        soup,
    ):

        html = soup.find("html")

        if html:

            return html.get(
                "lang",
                "",
            )

        return ""

    def extract_headings(
        self,
        soup,
    ):

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

        return headings

    def extract_meta_tags(
        self,
        soup,
    ):

        tags = {}

        for meta in soup.find_all("meta"):

            key = (
                meta.get("name")
                or meta.get("property")
                or meta.get("http-equiv")
            )

            value = meta.get("content")

            if key and value:

                tags[key] = value

        return tags

    def extract_images(
        self,
        soup,
    ):

        images = []

        for image in soup.find_all(
            "img",
            src=True,
        ):

            images.append(
                image["src"]
            )

        return images

    def extract_navigation(
        self,
        soup,
    ):

        navigation = []

        for nav in soup.find_all("nav"):

            for link in nav.find_all("a"):

                text = link.get_text(
                    " ",
                    strip=True,
                )

                if text:

                    navigation.append(text)

        return navigation

    def extract_text(
        self,
        soup,
    ):

        return soup.get_text(
            " ",
            strip=True,
        )


content_extractor = ContentExtractor()