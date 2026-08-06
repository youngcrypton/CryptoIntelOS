"""Focused tests for GitHub dependency intelligence."""

from src.github_intelligence import DependencyAnalyzer


def test_parser_detection_uses_manifest_registry() -> None:
    assert DependencyAnalyzer.detect_parser("services/api/requirements.txt") == "_parse_requirements"
    assert DependencyAnalyzer.detect_parser("package-lock.json") == "_parse_package_lock"
    assert DependencyAnalyzer.detect_parser("README.md") is None
    assert "Cargo.toml" in DependencyAnalyzer.supported_manifests()


def test_dependency_counting_merges_manifest_and_lockfile_entries() -> None:
    manifests = {
        "package.json": '{"dependencies":{"react":"18.3.1"},"devDependencies":{"vitest":"^2.0.0"}}',
        "package-lock.json": '{"packages":{"":{"dependencies":{"react":"18.3.1"}},"node_modules/react":{"version":"18.3.1"},"node_modules/scheduler":{"version":"0.23.2"}}}',
    }

    intelligence = DependencyAnalyzer().analyze_manifests(manifests)

    assert intelligence.dependency_count == 3
    assert intelligence.direct_dependencies == ("react", "vitest")
    assert intelligence.indirect_dependencies == ("scheduler",)
    assert intelligence.development_dependencies == ("vitest",)


def test_version_parsing_distinguishes_pins_and_ranges() -> None:
    assert DependencyAnalyzer.parse_version("==2.31.0") == ("==2.31.0", True)
    assert DependencyAnalyzer.parse_version("1.2.3") == ("1.2.3", True)
    assert DependencyAnalyzer.parse_version("^1.2.0") == ("^1.2.0", False)
    assert DependencyAnalyzer.parse_version(">=1.0,<2") == (">=1.0,<2", False)


def test_ecosystem_detection_across_manifests() -> None:
    manifests = {
        "requirements.txt": "requests==2.32.0\npytest>=8.0\n",
        "Cargo.toml": '[dependencies]\nserde = "1.0.0"\n',
        "go.mod": "module example.com/project\nrequire github.com/stretchr/testify v1.9.0\n",
    }

    intelligence = DependencyAnalyzer().analyze_manifests(manifests)

    assert intelligence.package_ecosystems == ("Python", "Rust", "Go")
    assert intelligence.dependency_count == 4
    assert set(intelligence.package_managers_used) == {"pip", "Cargo", "Go modules"}


def test_complexity_scoring_increases_with_transitive_load() -> None:
    simple = DependencyAnalyzer.complexity_score(5, 5, 0, 1, 1)
    complex_score = DependencyAnalyzer.complexity_score(200, 10, 190, 4, 5)

    assert simple < complex_score
    assert complex_score == 100.0
