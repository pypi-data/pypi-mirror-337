<img src="https://github.com/LucLor06/django-hyperscript/blob/main/django-hyperscript.png?raw=true" width=200>

# Django Hyperscript

This package is intended to simplify the process of dumping data from Django into Hyperscript by providing two template tags with options for customizing the output.

---
## Installation

1. Install using pip:
```bash
pip install hyperscript-dump
```

2. Add `django_hyperscript` to `INSTALLED_APPS` in your Django project's `settings.py`:
```python
# settings.py

INSTALLED_APPS = [
    ...,
    'django_hyperscript',
]
```

3. Load the tag library in the necessary templates:
```django
{% load hyperscript %}
```

---
## Usage

`build_hyperscript` turns python data into raw Hyperscript.

---
## Configuration

`build_hyperscript` has a set of additional keyword arguments to configure its behavior.

### `preserve`
*Type*: `bool` | *Default*: `False`

Keeps the element the Hyperscript is on in the DOM after initializing if `True`.

### `camelize`
*Type*: `bool` | *Default*: `True`

"Camelizes" dictionary keys from snake case (snake_case) to camel case (camelCase) to fit JavaScript naming conventions.

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
- The output is just the raw Hyperscript text since **`wrap`** is set to `False`

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
