# Wallet Discovery and Classification

## Discovery

`WalletDiscovery` consumes canonical `AdapterResult` output from the Blockchain Adapter SDK and produces immutable `WalletProfile` objects. Explicit metadata can describe wallet kind, including EOA, contract wallet, multisig, ENS name, name service, and labels. Discovery performs no network access, parsing, tracking, or inference.

## Classification

`WalletClassifier` applies deterministic keyword rules to wallet labels, ENS names, wallet kinds, and supplied metadata. It emits typed `WalletLabel` values for Founder, Team, Foundation, Treasury, VC, Smart Money, Exchange, Bridge, Market Maker, MEV, DAO, or Unknown. No AI or probabilistic inference participates.

## Runtime integration

`WalletRuntimeIntegration` forwards canonical runtime tuples through the existing Platform SDK `RuntimeFacade`. Runtime, Kernel, Platform SDK, Blockchain Platform, and Adapter SDK implementations remain unchanged.

## Future whale intelligence

Future Wallet Intelligence can add balance history, ownership graphs, flow analysis, entity resolution, and whale alerts around these stable profiles. Those capabilities belong to later application-layer sprints and must preserve deterministic provenance and canonical wallet ownership.
