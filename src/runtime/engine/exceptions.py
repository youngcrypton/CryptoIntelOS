class RuntimeExecutionError(Exception): pass
class PipelineError(RuntimeExecutionError): pass
class ExecutionError(RuntimeExecutionError): pass
class LifecycleError(RuntimeExecutionError): pass
class RegistrationError(RuntimeExecutionError): pass
