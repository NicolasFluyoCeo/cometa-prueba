import structlog

from .processors import process_logger


def setup_logger() -> None:
    """
    Set up the logger configuration using structlog.

    This function configures the logger with specific processors and parameters
    to enhance logging capabilities. It sets up callsite parameters, defines
    a list of processors for log processing, and configures structlog with
    these processors.

    The configuration includes:
    - Adding callsite parameters (pathname, line number, function name)
    - Merging context variables
    - Adding log levels and timestamps
    - Custom processing using process_logger
    - Renaming events and rendering to JSON

    Returns:
        None
    """
    callsite_params = {
        structlog.processors.CallsiteParameter.PATHNAME,
        structlog.processors.CallsiteParameter.LINENO,
        structlog.processors.CallsiteParameter.FUNC_NAME,
    }
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder(callsite_params),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        process_logger,
        structlog.processors.EventRenamer(to="msg", replace_by="event"),
        structlog.processors.JSONRenderer(),
    ]
    structlog.configure(
        processors=processors,
        cache_logger_on_first_use=True,
    )
