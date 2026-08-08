from src.cli import main
from src.providers.transports import RetryTransport

def test_cli_profile_execution(capsys):
    assert main(["project", "example", "--json"]) == 0
    assert '"runtime_state": "completed"' in capsys.readouterr().out

def test_retry_transport_uses_deterministic_backoff():
    calls=[]
    class T:
        def request(self, operation, **kwargs):
            calls.append(operation)
            if len(calls) < 2: raise RuntimeError("retry")
            return {"ok": True}
    assert RetryTransport(T(), sleeper=lambda delay: None).request("fixture")["ok"]
    assert len(calls) == 2
