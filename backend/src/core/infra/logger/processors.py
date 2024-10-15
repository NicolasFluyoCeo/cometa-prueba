from typing import Dict


def process_logger(_, __, event_dict: Dict) -> Dict:
    """
    Process and modify the event dictionary for logging.

    This function takes an event dictionary and modifies it by:
    1. Extracting specific keys (pathname, lineno, module, process, func_name)
    2. Adding new keys (file, line, tag) with values derived from the extracted ones
    3. Creating a tag by joining module, process, and func_name

    Args:
        _: Ignored parameter.
        __: Ignored parameter.
        event_dict (Dict): The event dictionary to be processed.

    Returns:
        Dict: The modified event dictionary.
    """
    pathname = event_dict.pop("pathname")
    lineno = event_dict.pop("lineno")
    module = event_dict.pop("module")
    process = event_dict.pop("process")
    func_name = event_dict.pop("func_name")

    event_dict["file"] = pathname
    event_dict["line"] = lineno
    event_dict["tag"] = "_".join([module, process, func_name])

    return event_dict
