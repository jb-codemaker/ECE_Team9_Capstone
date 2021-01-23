# 1. Style
Use [snake_case](https://en.wikipedia.org/wiki/Snake_case)

# 2. Variables
Variable names should say a little bit about what the variable is. For example use `transfer_function = ...` instead of `tf = ...`

Do Not update variables with the same name for example,

**DO NOT**
```python
example_variable = 2
.
.
.
example_variable = 4
```

**DO**
```python
example_variable = 2
.
.
.
double_example_variable = 4
```

This will be important with debugging so we don't have to follow variables around.

# 3. Functions
All functions will have [docstrings](https://www.python.org/dev/peps/pep-0257/)

The docstrings will have

* A brief description of what the function does.
* The arguments for the function and a brief description about those arguments.
* The return values for that function along with a brief description about those return values.

I think a good formatting option for us will be the [google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) style for docstrings **without the google TODO style**

```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
```
# 4. TODOs
Make sure TODOs look like `# TODO: example text`. This is so we can use the [snitch](https://github.com/tsoding/snitch) tool to automatically create issues for TODOs. 
You don't have to use the tool but its just nice to have.

# 5. Making a Pull Request

* Make sure the code does not fail when executed 
* Create TODOs in the code for unfinished work
