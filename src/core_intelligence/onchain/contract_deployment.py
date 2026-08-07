from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .block_reference import BlockReference
from .contract import Contract


@dataclass(frozen=True, slots=True)
class ContractDeployment(SerializableModel):
    deployment_id: str
    contract: Contract
    deployer: str
    block: BlockReference | None = None
