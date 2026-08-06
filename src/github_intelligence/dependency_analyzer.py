"""Repository dependency, ecosystem, and software supply-chain intelligence."""

import base64
import json
import re
import tomllib
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .client import GitHubClient
from .commit_analyzer import CommitIntelligence
from .release_analyzer import ReleaseIntelligence


@dataclass(frozen=True)
class DependencyRecord:
    """One normalized package dependency extracted from a repository manifest."""

    name: str
    version: str | None
    ecosystem: str
    package_manager: str
    direct: bool
    development: bool
    runtime: bool
    pinned: bool
    source_file: str


@dataclass(frozen=True)
class DependencyIntelligence:
    """Dependency inventory, health signals, scores, and supply-chain risks."""

    dependency_count: int
    direct_dependencies: tuple[str, ...]
    indirect_dependencies: tuple[str, ...]
    development_dependencies: tuple[str, ...]
    runtime_dependencies: tuple[str, ...]
    pinned_versions: tuple[str, ...]
    version_ranges: tuple[str, ...]
    package_ecosystems: tuple[str, ...]
    package_managers_used: tuple[str, ...]
    dependency_freshness: str
    outdated_dependencies: tuple[str, ...]
    abandoned_dependencies: tuple[str, ...]
    dependency_diversity: float
    package_ecosystem_maturity: str
    dependency_complexity: str
    deprecated_packages: tuple[str, ...]
    archived_packages: tuple[str, ...]
    suspicious_package_names: tuple[str, ...]
    typosquatting_indicators: tuple[str, ...]
    excessive_dependency_chains: bool
    dependency_explosion: bool
    unmaintained_libraries: tuple[str, ...]
    dependency_health_score: float
    supply_chain_risk_score: float
    dependency_complexity_score: float
    ecosystem_maturity_score: float
    package_freshness_score: float


@dataclass(frozen=True)
class _ParserDefinition:
    ecosystem: str
    package_manager: str
    parser: str


class DependencyAnalyzer:
    """Collect supported manifests and derive normalized dependency intelligence."""

    _PARSERS: dict[str, _ParserDefinition] = {
        "requirements.txt": _ParserDefinition("Python", "pip", "_parse_requirements"),
        "pyproject.toml": _ParserDefinition("Python", "pip/Poetry", "_parse_pyproject"),
        "poetry.lock": _ParserDefinition("Python", "Poetry", "_parse_poetry_lock"),
        "package.json": _ParserDefinition("JavaScript", "npm", "_parse_package_json"),
        "package-lock.json": _ParserDefinition("JavaScript", "npm", "_parse_package_lock"),
        "yarn.lock": _ParserDefinition("JavaScript", "Yarn", "_parse_yarn_lock"),
        "pnpm-lock.yaml": _ParserDefinition("JavaScript", "pnpm", "_parse_pnpm_lock"),
        "Cargo.toml": _ParserDefinition("Rust", "Cargo", "_parse_cargo_toml"),
        "Cargo.lock": _ParserDefinition("Rust", "Cargo", "_parse_cargo_lock"),
        "go.mod": _ParserDefinition("Go", "Go modules", "_parse_go_mod"),
        "go.sum": _ParserDefinition("Go", "Go modules", "_parse_go_sum"),
        "composer.json": _ParserDefinition("PHP", "Composer", "_parse_composer"),
        "Gemfile": _ParserDefinition("Ruby", "Bundler", "_parse_gemfile"),
        "Gemfile.lock": _ParserDefinition("Ruby", "Bundler", "_parse_gemfile_lock"),
    }
    _POPULAR_PACKAGES: dict[str, tuple[str, ...]] = {
        "Python": ("requests", "django", "flask", "numpy", "pandas", "pytest"),
        "JavaScript": ("react", "express", "lodash", "axios", "typescript", "webpack"),
        "Rust": ("serde", "tokio", "clap", "rand", "anyhow"),
        "Go": ("github.com/gin-gonic/gin", "github.com/stretchr/testify"),
        "PHP": ("laravel/framework", "symfony/console", "guzzlehttp/guzzle"),
        "Ruby": ("rails", "rake", "rspec", "bundler"),
    }

    def __init__(
        self,
        client: GitHubClient | None = None,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        """Initialize with reusable GitHub HTTP dependencies."""

        self.client = client or GitHubClient()
        self._opener = opener or urlopen

    def analyze(
        self,
        owner: str,
        repository: str,
        commits: CommitIntelligence | None = None,
        releases: ReleaseIntelligence | None = None,
        package_metadata: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> DependencyIntelligence:
        """Collect supported root manifests and analyze their dependencies."""

        owner_part = self._path_part(owner, "repository owner")
        repository_part = self._path_part(repository, "repository name")
        manifests: dict[str, str] = {}
        for filename in self.supported_manifests():
            content = self._fetch_manifest(owner_part, repository_part, filename)
            if content is not None:
                manifests[filename] = content
        return self.analyze_manifests(
            manifests,
            package_metadata=package_metadata,
            commits=commits,
            releases=releases,
        )

    def analyze_manifests(
        self,
        manifests: Mapping[str, str],
        package_metadata: Mapping[str, Mapping[str, Any]] | None = None,
        commits: CommitIntelligence | None = None,
        releases: ReleaseIntelligence | None = None,
        now: datetime | None = None,
    ) -> DependencyIntelligence:
        """Analyze supplied dependency manifests without network access."""

        records: list[DependencyRecord] = []
        detected_parsers: list[_ParserDefinition] = []
        for path, content in manifests.items():
            filename = path.replace("\\", "/").rsplit("/", 1)[-1]
            definition = self._PARSERS.get(filename)
            if definition is None:
                continue
            detected_parsers.append(definition)
            parser = getattr(self, definition.parser)
            records.extend(parser(content, filename, definition))

        dependencies = self._merge_records(records)
        metadata = package_metadata or {}
        reference_time = self._as_utc(now or datetime.now(timezone.utc))
        direct = [record for record in dependencies if record.direct]
        indirect = [record for record in dependencies if not record.direct]
        development = [record for record in dependencies if record.development]
        runtime = [record for record in dependencies if record.runtime]
        pinned = [record for record in dependencies if record.pinned]
        ranges = [
            record
            for record in dependencies
            if record.version and not record.pinned
        ]
        ecosystems = tuple(
            dict.fromkeys(definition.ecosystem for definition in detected_parsers)
        )
        managers = tuple(
            dict.fromkeys(definition.package_manager for definition in detected_parsers)
        )
        outdated = self._metadata_names(dependencies, metadata, "outdated")
        deprecated = self._metadata_names(dependencies, metadata, "deprecated")
        archived = self._metadata_names(dependencies, metadata, "archived")
        abandoned = self._abandoned_names(dependencies, metadata, reference_time)
        unmaintained = self._unmaintained_names(dependencies, metadata, reference_time)
        suspicious = tuple(
            record.name for record in dependencies if self._suspicious_name(record.name)
        )
        typosquatting = tuple(
            record.name
            for record in dependencies
            if self._typosquatting(record.name, record.ecosystem)
        )
        complexity_score = self.complexity_score(
            len(dependencies), len(direct), len(indirect), len(ecosystems), len(managers)
        )
        maturity_score = self._ecosystem_maturity_score(ecosystems, managers)
        freshness_score = self._freshness_score(
            dependencies, outdated, abandoned, metadata
        )
        chain_risk = len(indirect) >= 50 and len(indirect) > max(1, len(direct)) * 10
        explosion = len(dependencies) >= 200 or len(indirect) >= 150
        risk_score = self._supply_chain_risk_score(
            len(dependencies),
            deprecated,
            archived,
            suspicious,
            typosquatting,
            unmaintained,
            chain_risk,
            explosion,
        )
        health_score = round(
            max(
                0.0,
                min(
                    100.0,
                    0.4 * freshness_score
                    + 0.25 * maturity_score
                    + 0.2 * (100.0 - risk_score)
                    + 0.15 * (100.0 - complexity_score),
                ),
            ),
            2,
        )
        health_score = self._adjust_for_repository_health(
            health_score, commits, releases
        )
        diversity = round(min(100.0, len(ecosystems) / 4 * 100.0), 2)

        return DependencyIntelligence(
            dependency_count=len(dependencies),
            direct_dependencies=self._names(direct),
            indirect_dependencies=self._names(indirect),
            development_dependencies=self._names(development),
            runtime_dependencies=self._names(runtime),
            pinned_versions=self._versioned_names(pinned),
            version_ranges=self._versioned_names(ranges),
            package_ecosystems=ecosystems,
            package_managers_used=managers,
            dependency_freshness=self._quality_label(freshness_score),
            outdated_dependencies=outdated,
            abandoned_dependencies=abandoned,
            dependency_diversity=diversity,
            package_ecosystem_maturity=self._quality_label(maturity_score),
            dependency_complexity=self._complexity_label(complexity_score),
            deprecated_packages=deprecated,
            archived_packages=archived,
            suspicious_package_names=suspicious,
            typosquatting_indicators=typosquatting,
            excessive_dependency_chains=chain_risk,
            dependency_explosion=explosion,
            unmaintained_libraries=unmaintained,
            dependency_health_score=health_score,
            supply_chain_risk_score=risk_score,
            dependency_complexity_score=complexity_score,
            ecosystem_maturity_score=maturity_score,
            package_freshness_score=freshness_score,
        )

    @classmethod
    def supported_manifests(cls) -> tuple[str, ...]:
        """Return filenames understood by the parser registry."""

        return tuple(cls._PARSERS)

    @classmethod
    def detect_parser(cls, path: str) -> str | None:
        """Return the registered parser name for a manifest path."""

        filename = path.replace("\\", "/").rsplit("/", 1)[-1]
        definition = cls._PARSERS.get(filename)
        return definition.parser if definition else None

    @staticmethod
    def parse_version(value: object) -> tuple[str | None, bool]:
        """Normalize a version expression and identify exact pins."""

        if isinstance(value, Mapping):
            value = value.get("version")
        if value is None:
            return None, False
        version = str(value).strip()
        if not version or version in {"*", "latest"}:
            return version or None, False
        pinned = bool(
            re.fullmatch(r"(?:==|=)?v?\d+(?:\.\d+){1,3}(?:[-+][0-9A-Za-z.-]+)?", version)
        )
        return version, pinned

    @staticmethod
    def complexity_score(
        total: int,
        direct: int,
        indirect: int,
        ecosystems: int,
        managers: int,
    ) -> float:
        """Score dependency complexity from volume, transitive load, and tooling."""

        if total <= 0:
            return 0.0
        volume = min(45.0, total / 200 * 45.0)
        transitive = min(35.0, indirect / max(1, direct) / 10 * 35.0)
        ecosystem_load = min(10.0, max(0, ecosystems - 1) * 3.5)
        manager_load = min(10.0, max(0, managers - 1) * 2.5)
        return round(min(100.0, volume + transitive + ecosystem_load + manager_load), 2)

    def _parse_requirements(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        for raw_line in content.splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if not line or line.startswith(("-", "http:", "https:", "git+")):
                continue
            match = re.match(r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)", line)
            if match:
                records.append(
                    self._record(match.group(1), match.group(2), definition, filename)
                )
        return records

    def _parse_pyproject(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._toml(content)
        records: list[DependencyRecord] = []
        project = data.get("project", {})
        if isinstance(project, Mapping):
            for value in project.get("dependencies", []) or []:
                parsed = self._requirement_parts(str(value))
                if parsed:
                    records.append(self._record(*parsed, definition, filename))
            optional = project.get("optional-dependencies", {})
            if isinstance(optional, Mapping):
                for group, values in optional.items():
                    for value in values if isinstance(values, list) else []:
                        parsed = self._requirement_parts(str(value))
                        if parsed:
                            records.append(
                                self._record(
                                    *parsed,
                                    definition,
                                    filename,
                                    development=self._development_group(str(group)),
                                )
                            )
        tool = data.get("tool", {})
        poetry = tool.get("poetry", {}) if isinstance(tool, Mapping) else {}
        if isinstance(poetry, Mapping):
            records.extend(
                self._mapping_dependencies(
                    poetry.get("dependencies", {}), definition, filename, excluded={"python"}
                )
            )
            records.extend(
                self._mapping_dependencies(
                    poetry.get("dev-dependencies", {}), definition, filename, development=True
                )
            )
            groups = poetry.get("group", {})
            if isinstance(groups, Mapping):
                for group, group_data in groups.items():
                    dependencies = group_data.get("dependencies", {}) if isinstance(group_data, Mapping) else {}
                    records.extend(
                        self._mapping_dependencies(
                            dependencies,
                            definition,
                            filename,
                            development=self._development_group(str(group)),
                        )
                    )
        return records

    def _parse_poetry_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._toml(content)
        packages = data.get("package", [])
        return [
            self._record(
                str(package.get("name")),
                str(package.get("version") or ""),
                definition,
                filename,
                direct=False,
                development=str(package.get("category", "main")) == "dev",
            )
            for package in packages if isinstance(package, Mapping) and package.get("name")
        ] if isinstance(packages, list) else []

    def _parse_package_json(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._json(content)
        records = self._mapping_dependencies(data.get("dependencies", {}), definition, filename)
        records.extend(self._mapping_dependencies(data.get("optionalDependencies", {}), definition, filename))
        records.extend(self._mapping_dependencies(data.get("peerDependencies", {}), definition, filename))
        records.extend(self._mapping_dependencies(data.get("devDependencies", {}), definition, filename, development=True))
        return records

    def _parse_package_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._json(content)
        records: list[DependencyRecord] = []
        packages = data.get("packages", {})
        root = packages.get("", {}) if isinstance(packages, Mapping) else {}
        direct_names = set()
        if isinstance(root, Mapping):
            direct_names.update((root.get("dependencies") or {}).keys())
            direct_names.update((root.get("devDependencies") or {}).keys())
        if isinstance(packages, Mapping):
            for path, value in packages.items():
                if not path or not isinstance(value, Mapping):
                    continue
                name = str(value.get("name") or str(path).rsplit("node_modules/", 1)[-1])
                records.append(
                    self._record(
                        name,
                        value.get("version"),
                        definition,
                        filename,
                        direct=name in direct_names,
                        development=bool(value.get("dev", False)),
                    )
                )
        return records

    def _parse_yarn_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        current_names: list[str] = []
        for line in content.splitlines():
            if line and not line[0].isspace() and line.rstrip().endswith(":"):
                current_names = [self._yarn_name(value) for value in line[:-1].split(",")]
            elif current_names and line.strip().startswith("version "):
                version = line.strip()[8:].strip('"\'')
                records.extend(
                    self._record(name, version, definition, filename, direct=False)
                    for name in current_names if name
                )
                current_names = []
        return records

    def _parse_pnpm_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        for line in content.splitlines():
            match = re.match(r"\s{2,}['\"]?/?(@?[^@'\"\s:]+(?:/[^@'\"\s:]+)?)@([^:'\"\s]+)['\"]?:", line)
            if match:
                records.append(
                    self._record(match.group(1), match.group(2), definition, filename, direct=False)
                )
        return records

    def _parse_cargo_toml(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._toml(content)
        records: list[DependencyRecord] = []
        for section, development in (("dependencies", False), ("dev-dependencies", True), ("build-dependencies", True)):
            records.extend(
                self._mapping_dependencies(data.get(section, {}), definition, filename, development=development)
            )
        return records

    def _parse_cargo_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._toml(content)
        packages = data.get("package", [])
        return [
            self._record(str(item.get("name")), item.get("version"), definition, filename, direct=False)
            for item in packages if isinstance(item, Mapping) and item.get("name")
        ] if isinstance(packages, list) else []

    def _parse_go_mod(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        in_require = False
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if line == "require (":
                in_require = True
                continue
            if in_require and line == ")":
                in_require = False
                continue
            if line.startswith("require "):
                line = line[8:].strip()
            elif not in_require:
                continue
            parts = line.split()
            if len(parts) >= 2:
                indirect = "// indirect" in line
                records.append(
                    self._record(parts[0], parts[1], definition, filename, direct=not indirect)
                )
        return records

    def _parse_go_sum(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        seen: set[tuple[str, str]] = set()
        for line in content.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                version = parts[1].removesuffix("/go.mod")
                key = (parts[0], version)
                if key not in seen:
                    seen.add(key)
                    records.append(
                        self._record(parts[0], version, definition, filename, direct=False)
                    )
        return records

    def _parse_composer(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        data = self._json(content)
        excluded = {"php"}
        records = self._mapping_dependencies(data.get("require", {}), definition, filename, excluded=excluded)
        records.extend(self._mapping_dependencies(data.get("require-dev", {}), definition, filename, development=True, excluded=excluded))
        return [record for record in records if not record.name.startswith("ext-")]

    def _parse_gemfile(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        development = False
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if line.startswith("group "):
                development = self._development_group(line)
            elif line == "end":
                development = False
            match = re.match(r"gem\s+['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", line)
            if match:
                records.append(
                    self._record(match.group(1), match.group(2), definition, filename, development=development)
                )
        return records

    def _parse_gemfile_lock(
        self, content: str, filename: str, definition: _ParserDefinition
    ) -> list[DependencyRecord]:
        records: list[DependencyRecord] = []
        direct_names: set[str] = set()
        in_dependencies = False
        for line in content.splitlines():
            if line == "DEPENDENCIES":
                in_dependencies = True
                continue
            if in_dependencies:
                if line and not line.startswith(" "):
                    in_dependencies = False
                else:
                    match = re.match(r"\s{2}([^\s(!]+)", line)
                    if match:
                        direct_names.add(match.group(1))
            match = re.match(r"\s{4}([^\s(]+) \(([^)]+)\)", line)
            if match:
                records.append(
                    self._record(match.group(1), match.group(2), definition, filename, direct=False)
                )
        return [
            DependencyRecord(
                **{**record.__dict__, "direct": record.name in direct_names}
            )
            for record in records
        ]

    def _mapping_dependencies(
        self,
        values: object,
        definition: _ParserDefinition,
        filename: str,
        development: bool = False,
        excluded: set[str] | None = None,
    ) -> list[DependencyRecord]:
        if not isinstance(values, Mapping):
            return []
        excluded_names = excluded or set()
        return [
            self._record(
                str(name), value, definition, filename, development=development
            )
            for name, value in values.items()
            if str(name) not in excluded_names
        ]

    def _record(
        self,
        name: str,
        version: object,
        definition: _ParserDefinition,
        filename: str,
        direct: bool = True,
        development: bool = False,
    ) -> DependencyRecord:
        normalized_version, pinned = self.parse_version(version)
        return DependencyRecord(
            name=name.strip(),
            version=normalized_version,
            ecosystem=definition.ecosystem,
            package_manager=definition.package_manager,
            direct=direct,
            development=development,
            runtime=not development,
            pinned=pinned,
            source_file=filename,
        )

    @staticmethod
    def _merge_records(records: Iterable[DependencyRecord]) -> list[DependencyRecord]:
        merged: dict[tuple[str, str], DependencyRecord] = {}
        for record in records:
            key = (record.ecosystem, record.name.casefold())
            existing = merged.get(key)
            if existing is None or (record.direct and not existing.direct):
                merged[key] = record
            elif existing.version is None and record.version is not None:
                merged[key] = DependencyRecord(
                    name=existing.name,
                    version=record.version,
                    ecosystem=existing.ecosystem,
                    package_manager=existing.package_manager,
                    direct=existing.direct,
                    development=existing.development,
                    runtime=existing.runtime,
                    pinned=record.pinned,
                    source_file=existing.source_file,
                )
        return list(merged.values())

    def _fetch_manifest(self, owner: str, repository: str, filename: str) -> str | None:
        request = self.client.prepare_request(
            f"/repos/{owner}/{repository}/contents/{quote(filename)}"
        )
        try:
            payload, headers = self._fetch(request)
        except HTTPError as error:
            if error.code == 404:
                return None
            raise
        if not isinstance(payload, Mapping) or payload.get("type") != "file":
            return None
        content = payload.get("content")
        if not isinstance(content, str):
            return None
        encoding = payload.get("encoding")
        return base64.b64decode(content).decode("utf-8") if encoding == "base64" else content

    def _fetch(self, request: Request) -> tuple[Any, Mapping[str, str]]:
        self.client.rate_limiter.ensure_available()
        with self._opener(request, timeout=self.client.config.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            headers = response.headers
        self._update_rate_limit(headers)
        return payload, headers

    def _update_rate_limit(self, headers: Mapping[str, str]) -> None:
        remaining = headers.get("X-RateLimit-Remaining")
        used = headers.get("X-RateLimit-Used")
        reset = headers.get("X-RateLimit-Reset")
        if remaining is not None and used is not None and reset is not None:
            self.client.rate_limiter.update(
                self._integer(remaining), self._integer(used), self._integer(reset)
            )

    @staticmethod
    def _metadata_names(
        dependencies: Iterable[DependencyRecord],
        metadata: Mapping[str, Mapping[str, Any]],
        field: str,
    ) -> tuple[str, ...]:
        return tuple(
            record.name for record in dependencies if bool(metadata.get(record.name, {}).get(field))
        )

    @classmethod
    def _abandoned_names(
        cls,
        dependencies: Iterable[DependencyRecord],
        metadata: Mapping[str, Mapping[str, Any]],
        now: datetime,
    ) -> tuple[str, ...]:
        return tuple(
            record.name
            for record in dependencies
            if metadata.get(record.name, {}).get("archived")
            or cls._metadata_age(metadata.get(record.name, {}).get("last_updated"), now) >= 730
        )

    @classmethod
    def _unmaintained_names(
        cls,
        dependencies: Iterable[DependencyRecord],
        metadata: Mapping[str, Mapping[str, Any]],
        now: datetime,
    ) -> tuple[str, ...]:
        return tuple(
            record.name
            for record in dependencies
            if cls._metadata_age(metadata.get(record.name, {}).get("last_updated"), now) >= 365
        )

    @staticmethod
    def _metadata_age(value: object, now: datetime) -> int:
        if not isinstance(value, str):
            return -1
        try:
            timestamp = DependencyAnalyzer._as_utc(
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            )
        except ValueError:
            return -1
        return max(0, (now - timestamp).days)

    @staticmethod
    def _suspicious_name(name: str) -> bool:
        normalized = name.casefold()
        return bool(
            len(name) > 80
            or re.search(r"(?:free|official|secure|wallet)[-_]?(?:crypto|token|login)", normalized)
            or normalized.count("-") >= 5
            or re.search(r"(.)\1{4,}", normalized)
        )

    @classmethod
    def _typosquatting(cls, name: str, ecosystem: str) -> bool:
        normalized = name.casefold()
        return any(
            normalized != popular.casefold()
            and cls._edit_distance(normalized, popular.casefold()) == 1
            for popular in cls._POPULAR_PACKAGES.get(ecosystem, ())
        )

    @staticmethod
    def _edit_distance(left: str, right: str) -> int:
        if abs(len(left) - len(right)) > 1:
            return 2
        previous = list(range(len(right) + 1))
        for index, left_character in enumerate(left, start=1):
            current = [index]
            for other_index, right_character in enumerate(right, start=1):
                current.append(
                    min(
                        current[-1] + 1,
                        previous[other_index] + 1,
                        previous[other_index - 1] + (left_character != right_character),
                    )
                )
            previous = current
        return previous[-1]

    @staticmethod
    def _ecosystem_maturity_score(
        ecosystems: tuple[str, ...], managers: tuple[str, ...]
    ) -> float:
        if not ecosystems:
            return 0.0
        established = {"Python", "JavaScript", "Rust", "Go", "PHP", "Ruby"}
        ecosystem_score = sum(value in established for value in ecosystems) / len(ecosystems) * 80
        lock_manager_bonus = min(20.0, len(managers) * 5.0)
        return round(min(100.0, ecosystem_score + lock_manager_bonus), 2)

    @staticmethod
    def _freshness_score(
        dependencies: list[DependencyRecord],
        outdated: tuple[str, ...],
        abandoned: tuple[str, ...],
        metadata: Mapping[str, Mapping[str, Any]],
    ) -> float:
        if not dependencies:
            return 0.0
        known = sum(record.name in metadata for record in dependencies)
        penalty = len(outdated) * 8.0 + len(abandoned) * 18.0
        coverage_adjustment = 70.0 + known / len(dependencies) * 30.0
        return round(max(0.0, min(100.0, coverage_adjustment - penalty)), 2)

    @staticmethod
    def _supply_chain_risk_score(
        total: int,
        deprecated: tuple[str, ...],
        archived: tuple[str, ...],
        suspicious: tuple[str, ...],
        typosquatting: tuple[str, ...],
        unmaintained: tuple[str, ...],
        chain_risk: bool,
        explosion: bool,
    ) -> float:
        if total <= 0:
            return 0.0
        score = (
            len(deprecated) * 8
            + len(archived) * 12
            + len(suspicious) * 15
            + len(typosquatting) * 20
            + len(unmaintained) * 6
            + (15 if chain_risk else 0)
            + (20 if explosion else 0)
        )
        return round(min(100.0, float(score)), 2)

    @staticmethod
    def _adjust_for_repository_health(
        score: float,
        commits: CommitIntelligence | None,
        releases: ReleaseIntelligence | None,
    ) -> float:
        adjustment = 0.0
        if commits and commits.abandoned_repository:
            adjustment -= 10.0
        if releases and releases.abandoned_releases:
            adjustment -= 10.0
        return round(max(0.0, min(100.0, score + adjustment)), 2)

    @staticmethod
    def _names(records: Iterable[DependencyRecord]) -> tuple[str, ...]:
        return tuple(record.name for record in records)

    @staticmethod
    def _versioned_names(records: Iterable[DependencyRecord]) -> tuple[str, ...]:
        return tuple(f"{record.name}{record.version or ''}" for record in records)

    @staticmethod
    def _quality_label(score: float) -> str:
        if score >= 80:
            return "high"
        if score >= 60:
            return "moderate"
        if score >= 40:
            return "low"
        return "poor"

    @staticmethod
    def _complexity_label(score: float) -> str:
        if score >= 75:
            return "very_high"
        if score >= 50:
            return "high"
        if score >= 25:
            return "moderate"
        return "low"

    @staticmethod
    def _requirement_parts(value: str) -> tuple[str, str] | None:
        match = re.match(r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)", value)
        return (match.group(1), match.group(2)) if match else None

    @staticmethod
    def _development_group(value: str) -> bool:
        normalized = value.casefold()
        return any(marker in normalized for marker in ("dev", "test", "lint", "docs"))

    @staticmethod
    def _yarn_name(value: str) -> str:
        normalized = value.strip().strip('"\'')
        if normalized.startswith("@"):
            parts = normalized.rsplit("@", 1)
            return parts[0] if len(parts) == 2 else normalized
        return normalized.split("@", 1)[0]

    @staticmethod
    def _json(content: str) -> Mapping[str, Any]:
        try:
            value = json.loads(content)
        except json.JSONDecodeError:
            return {}
        return value if isinstance(value, Mapping) else {}

    @staticmethod
    def _toml(content: str) -> Mapping[str, Any]:
        try:
            return tomllib.loads(content)
        except tomllib.TOMLDecodeError:
            return {}

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _path_part(value: str, label: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{label} must not be empty")
        if "/" in normalized:
            raise ValueError(f"{label} must be a single path component")
        return normalized

    @staticmethod
    def _integer(value: object) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0
