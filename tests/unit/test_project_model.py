from src.models.project import Project


def test_project_creation():
    """Test that a Project object is created correctly."""

    project = Project(
        id=1,
        name="Bitcoin",
        website="https://bitcoin.org",
        blockchain="Bitcoin",
        category="Layer 1",
        status="Active",
    )

    assert project.id == 1
    assert project.name == "Bitcoin"
    assert project.website == "https://bitcoin.org"
    assert project.blockchain == "Bitcoin"
    assert project.category == "Layer 1"
    assert project.status == "Active"


def test_project_dataclass_fields():
    """Ensure all expected fields exist."""

    project = Project(
        id=2,
        name="Ethereum",
        website="https://ethereum.org",
        blockchain="Ethereum",
        category="Smart Contract",
        status="Active",
    )

    assert hasattr(project, "id")
    assert hasattr(project, "name")
    assert hasattr(project, "website")
    assert hasattr(project, "blockchain")
    assert hasattr(project, "category")
    assert hasattr(project, "status")


def test_project_string_values():
    """Verify field values remain unchanged."""

    project = Project(
        id=3,
        name="Solana",
        website="https://solana.com",
        blockchain="Solana",
        category="Layer 1",
        status="Monitoring",
    )

    assert project.name == "Solana"
    assert project.status == "Monitoring"