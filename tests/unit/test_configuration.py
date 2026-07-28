from pathlib import Path

from src.core.config import Config


def test_config_initialization():
    """Verify Config initializes correctly."""

    config = Config()

    assert config is not None
    assert isinstance(config.project_root, Path)


def test_project_directories():
    """Verify required project directories are configured."""

    config = Config()

    assert config.data_dir.name == "data"
    assert config.logs_dir.name == "logs"
    assert config.assets_dir.name == "assets"
    assert config.docs_dir.name == "docs"


def test_default_environment():
    """Verify default environment value."""

    config = Config()

    assert config.environment in [
        "development",
        "production",
        "testing",
    ]


def test_version_exists():
    """Verify version string exists."""

    config = Config()

    assert isinstance(config.version, str)
    assert len(config.version) > 0


def test_verify_directories():
    """Verify required directories are created."""

    config = Config()

    config.verify_directories()

    assert config.data_dir.exists()
    assert config.logs_dir.exists()
    assert config.assets_dir.exists()
    assert config.docs_dir.exists()