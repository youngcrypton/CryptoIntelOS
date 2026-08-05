from src.orchestrator.orchestrator import orchestrator


orchestrator.load_collectors()

orchestrator.run()