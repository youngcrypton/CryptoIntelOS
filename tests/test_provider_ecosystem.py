from src.core_intelligence.models import Observation
from datetime import UTC, datetime
from src.providers.connectors import *
from src.providers.providers import *
from src.providers.adapters import *
from src.providers.management import *

NOW = datetime(2026, 8, 8, tzinfo=UTC)

class ConnectorFixture:
    metadata = ConnectorMetadata("fixture-connector", "Fixture")
    def request(self, operation, context, policy): return ConnectorResult(self.metadata.connector_id, True, {"operation": operation})
class ProviderFixture:
    metadata = ProviderMetadata("fixture-provider", "Fixture", source="fixture")
    def normalize(self, result, context, policy): return ProviderResult(self.metadata.provider_id, result.success, result.payload, provenance=(("connector", result.connector_id),))
class AdapterFixture:
    metadata = AdapterMetadata("fixture-adapter", "Fixture")
    def adapt(self, result, context):
        observation = Observation("observation-1", context.source, "fixture", "1", NOW, NOW, "1", "checksum", result.value)
        return AdapterResult(self.metadata.adapter_id, (observation,), result.provenance)

def test_connector_provider_adapter_and_management_flow():
    connector, provider, adapter = ConnectorFixture(), ProviderFixture(), AdapterFixture()
    manager = ProviderManager()
    execution = manager.execute(connector, provider, adapter, "collect", "execution-1", "correlation-1")
    projection = ProviderRuntimeProjection().project(execution.result)
    assert projection[0].observation_id == "observation-1"
    assert execution.result.provenance == (("connector", "fixture-connector"),)

def test_registries_capability_health_and_selection():
    connectors = ConnectorRegistry(); connectors.register(ConnectorFixture())
    providers = ProviderRegistry(); providers.register(ProviderFixture())
    assert connectors.get("fixture-connector") is not None
    assert ProviderSelector().select(providers.all()) is not None
    assert CapabilityNegotiator().supports(("collect",), ("collect",))
    health = HealthManager(); health.record("fixture-provider", ProviderHealth(ProviderStatus.HEALTHY))
    assert health.available("fixture-provider")
