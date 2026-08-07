"""Canonical identifier categories."""
from enum import StrEnum

class IdentifierType(StrEnum):
    GITHUB_REPOSITORY_ID = "github_repository_id"
    URL = "url"
    TWITTER_USERNAME = "twitter_username"
    WALLET_ADDRESS = "wallet_address"
    ENS_NAME = "ens_name"
    WEBSITE_DOMAIN = "website_domain"
    DISCORD_INVITE = "discord_invite"
    TELEGRAM_USERNAME = "telegram_username"
    EXTERNAL_ID = "external_id"
