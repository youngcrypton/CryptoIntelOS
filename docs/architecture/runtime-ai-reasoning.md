# Runtime AI Reasoning Engine

The reasoning engine transforms correlated canonical intelligence into explainable conclusions. It consumes Runtime and Kernel contracts only, never raw collector payloads, and never owns truth.

Requests, prompts, memory, policies, chains, steps, explanations, and confidence are provider-neutral immutable contracts. `ReasoningProvider` isolates OpenAI, Anthropic, Gemini, DeepSeek, Ollama, Llama.cpp, or future local providers. `ReasoningStrategy` supports rule-based, hybrid, LLM, retrieval-augmented, and graph reasoning implementations without embedding vendor behavior.

Evidence references, assumptions, limitations, confidence sources, and provenance make conclusions auditable. Chains preserve the reasoning path. Versioned memory and policy references support future RAG, multi-model, and distributed execution. `ReasoningEngine` only delegates to a supplied strategy.
