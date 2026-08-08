from pathlib import Path

from tools import validate_repository


def test_pytest_discovers_legacy_and_standard_test_names() -> None:
    config = Path("pytest.ini").read_text(encoding="utf-8")
    assert "test_*.py *_test.py" in config


def test_docker_module_entry_point_exists() -> None:
    from src.__main__ import main

    assert Path("src/__main__.py").is_file()
    assert 'CMD ["python", "-m", "src"]' in Path("Dockerfile").read_text(encoding="utf-8")
    assert callable(main)


def test_repository_validator_checks_are_callable() -> None:
    validate_repository.check_model_ownership()
    validate_repository.check_runtime_boundaries()


def test_repository_packages_are_importable() -> None:
    validate_repository.check_imports()
