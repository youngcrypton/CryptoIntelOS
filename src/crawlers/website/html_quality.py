from bs4 import BeautifulSoup


class HtmlQualityAnalyzer:
    """
    Scores HTML quality.

    Higher score = better page.
    """

    def score(self, html):

        if not html:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        score = 0

        text = soup.get_text(" ", strip=True)

        score += len(text)

        score += len(soup.find_all("a")) * 5

        score += len(soup.find_all("img")) * 3

        score += len(soup.find_all(["h1", "h2", "h3"])) * 10

        score += len(soup.find_all("script"))

        return score


html_quality = HtmlQualityAnalyzer()