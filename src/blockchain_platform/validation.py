from dataclasses import dataclass
from typing import Protocol, TypeVar

from .models import Blockchain, ChainEndpoint, ChainMetadata


@dataclass(frozen=True, slots=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


ValidatedModel = TypeVar("ValidatedModel", Blockchain, ChainEndpoint, ChainMetadata)


class BlockchainModelValidator(Protocol[ValidatedModel]):
    def validate(self, value: ValidatedModel) -> ValidationResult: ...


class BlockchainValidator(BlockchainModelValidator[Blockchain], Protocol): ...
class ChainEndpointValidator(BlockchainModelValidator[ChainEndpoint], Protocol): ...
class ChainMetadataValidator(BlockchainModelValidator[ChainMetadata], Protocol): ...
