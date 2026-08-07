"""Canonical entity categories."""
from enum import StrEnum

class EntityType(StrEnum):
    PROJECT = "project"
    ORGANIZATION = "organization"
    PERSON = "person"
    ACCOUNT = "account"
    REPOSITORY = "repository"
    WALLET = "wallet"
    TOKEN = "token"
    PROTOCOL = "protocol"
    DOMAIN = "domain"
    COMMUNITY = "community"
    UNKNOWN = "unknown"
