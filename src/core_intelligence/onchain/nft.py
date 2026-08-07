from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .nft_collection import NFTCollection


@dataclass(frozen=True, slots=True)
class NFT(SerializableModel):
    nft_id: str
    collection: NFTCollection
    token_identifier: str
    owner: str | None = None
