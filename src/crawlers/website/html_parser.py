from bs4 import BeautifulSoup


class HTMLParser:
    """
    Converts raw HTML into BeautifulSoup.
    """

    def parse(self, html):

        return BeautifulSoup(
            html,
            "html.parser",
        )


html_parser = HTMLParser()