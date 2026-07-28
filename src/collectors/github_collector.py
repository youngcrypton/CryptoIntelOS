from github import Auth, Github

from src.collectors.base.base_collector import BaseCollector
from src.core.config import config


class GitHubCollector(BaseCollector):
    """
    GitHub Intelligence Collector.
    """

    def __init__(self):
        super().__init__("GitHub")
        self.client = None

    def connect(self):
        """
        Create the GitHub client only when needed.
        """

        if self.client is None:

            auth = Auth.Token(config.github_token)

            self.client = Github(auth=auth)

    def collect(self):

        self.connect()

        print("\nConnecting to GitHub...")

        user = self.client.get_user()

        print(f"Authenticated as: {user.login}")

        return user

    def normalize(self, data):

        return data


github_collector = GitHubCollector()