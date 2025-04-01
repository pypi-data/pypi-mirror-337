# Hyperscript Dump

Hyperscript dump is a simple python library for turning python data into raw hyperscript.

---
## Installation

1. Install using pip:
```bash
pip install hyperscript-dump
```

2. Import and use `build_hyperscript` where needed
```python
from hyperscript_dump import build_hyperscript
```

---
## Usage

`build_hyperscript` turns python data into raw Hyperscript.

```python
build_hyperscript(data, name='myData')
```
will return hyperscript like:
```python
"""
init
    set global myData to {'key': 'value'}
    then remove me
end
"""
```

---
## Configuration

`build_hyperscript` has a set of additional keyword arguments to configure its behavior.

### `preserve`
*Type*: `bool` | *Default*: `False`

Keeps the element the Hyperscript is on in the DOM after initializing if `True`.

### `camelize`
*Type*: `bool` | *Default*: `True`

"Camelizes" dictionary keys from snake case (snake_case) to camel case (camelCase) to fit JavaScript naming conventions.

### `flatten`
*Type*: `bool` | *Default*: `False`

Each key value pair in a dictionary is assigned as a separate variable, rather than as a single object.

**Note:** Requires data to be a dictionary.

### `scope`
*Type*: `str` | *Default*: `global`

Determines the scope of the Hyperscript variable (global, element, or local).

### `event`
*Type*: `str` | *Default*: `init`

Specifies the event that triggers assignment. The Hyperscript "on" keyword should not need be provided.

**Note:** If **`preserve`** is `False` (which it is by default), the element will not be removed until after the event is fired and values are set.

### `debug`
*Type*: `bool` | *Default*: `False`

Logs the set variable name(s) and value(s).

## Final example
```python
build_hyperscript(data, 'myData', preserve=True, camelize=False, scope='element')
```
assuming `data` is `{"my_value": 25}`, the tag would output
```python
"init set element my_data to {'my_value': 25} end"
```
In this example:
- The Hyperscript remains in the DOM since **`preserve`** is `True`
- The keys within the dumped data remain in snake case since **`camelize`** is `False`
- The variable is scoped to the element the Hyperscript belongs to since **`scope`** is set to `'element'`

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
