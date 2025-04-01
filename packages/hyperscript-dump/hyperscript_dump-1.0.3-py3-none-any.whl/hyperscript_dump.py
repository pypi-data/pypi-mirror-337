import json
from typing import Any

__version__ = '1.0.3'

def _snake_case_to_camel_case(data: str) -> str:
    words = data.split('_')
    return f"{words[0]}{''.join([word.capitalize() for word in words[1:]])}"

def _camelize(data: dict) -> dict:
    if isinstance(data, dict):
        return {
            _snake_case_to_camel_case(key): _camelize(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [_camelize(item) for item in data]
    else:
        return data
    
def _prepare_for_hyperscript(value):
    value = json.dumps(value)
    return value
    
def build_hyperscript(
    data: Any,
    name: str = 'data',
    *,
    preserve: bool = False,
    flatten: bool = False,
    camelize: bool = True,
    scope: str = 'global',
    debug: bool = False,
    event: str = 'init'
) -> str:
    """
    Generate a Hyperscript block from Python data.

    Args:
        data: The Python data to assign.
        name: The name of the variable (ignored if flatten=True).
        preserve: If False, the element will remove itself after execution.
        flatten: If True, each key in a dict becomes a separate variable.
        camelize: If True, converts snake_case keys to camelCase.
        scope: Hyperscript scope (e.g., "global", "local", "element").
        debug: If True, adds console logging.
        event: The triggering event (or "init").

    Returns:
        A string of valid Hyperscript code.
    """
    event = f'on {event}' if event not in ['init', None] else 'init'

    if camelize:
        data = _camelize(data)

    if flatten:
        if not isinstance(data, dict):
            raise TypeError(
                f'Invalid type for mapping: expected dict, got {type(data).__name__}'
            )
        
        assignments = []
        for key, value in data.items():
            value = _prepare_for_hyperscript(value)
            assignment = f'set {scope} {key} to {value}'
            if debug:
                logging_statement = f'call console.log(`{key}:\\n`, {key})'
                assignment = f'{assignment} then {logging_statement}'
            assignments.append(assignment)
        assignment = '\n    '.join(assignments)
        
    else:
        data = _prepare_for_hyperscript(data)
        assignment = f'set {scope} {name} to {data}'
        if debug:
            logging_statement = f'call console.log(`{name}:\\n`, {name})'
            assignment = f'{assignment} then {logging_statement}'

    hyperscript = f'{event}\n    {assignment}'

    if not preserve:
        hyperscript = f'{hyperscript} then remove me'  

    hyperscript = f'{hyperscript}\nend'
    return hyperscript