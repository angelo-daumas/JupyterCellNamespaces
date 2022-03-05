# JupyterCellNamespaces
A module that allows you to create block-scoped namespaces in Python (intended for use in Jupyter cells)

## Special variables:

* `globals()`: this is the built-in python function. Namespace-specific variables will be stored here and then removed when the `with` statement is exited.
* `G`: this global variable will contain the global state before entering the `with` statement. It can also be used to set global variables.
* `NS`: in the examples below, this represents the `Namespace` that is currently active. In order to actually store variables for future use in this namespace, they must be declared as `NS.variable_name = `. If they are simply declared as `variable_name = `, they will only exist inside of the current block and won't be present if the same namespace is used in another `with` block.


## Usage:

This module will generally be used by "activating" namespaces inside of an `with` block.

### Using a one-time-only namespace:
You can limit the scope of variables so that they only exist inside of the `with` block, without having to actually name a `Namespace` object. You can still declare globals by using the G object. If you specify the enable parameter `use_namespace(enable=False)`, then you can disable scoping for testing purposes.

```python
with use_namespace():
  abc = 2
  G.cba = 0
  print(abc)  # will print 2 on the console.
  print(cba)  # will print 0 on the console.

abc  # ERROR: Will not exist.
cba  # Will be equal to 0.
```

```python
with use_namespace(False):
  abc = 2
  G.cba = 0
  print(abc)  # will print 2 on the console.
  print(cba)  # will print 0 on the console.

abc  # Will be equal to 2.
cba  # Will be equal to 0.
```

### Using the `use_namespace` function:

```python
with use_namespace(name='my_namespace') as NS:
  abc = 2
  print(abc)  # will print 2 on the console.

abc  # ERROR: Will not exist.
namespaces.my_namespace.abc  # ERROR: Will not exist.
```


### Accessing the `namespaces` variable:
Namespaces can be stored in the `namespaces` variable. They can be called in an `with` statement in order to be activated. If a namespace with that name does not exist in the `namespaces` variable, it will be automatically created.

```python
with namespaces.my_namespace() as NS:
  G.abc = 2
  print(abc)  # will print 2 on the console.

abc  # Will be equal to 2.
namespaces.my_namespace.abc  # ERROR: Will not exist.
```

### Creating a `Namespace` directly:
It is also possible to create a Namespace object that is not stored in the `namespaces` variable.

```python
NS = Namespace()
with NS():
  NS.abc = 2
  print(abc)  # will print 2 on the console.

NS.abc  # Will be equal to 2
abc  # ERROR: Will not exist.
```

## Limitations

* Not compatible with functions (globals used inside functions will always be scoped to the current namespace, even if they were declared in a previous one)
* Variables get marked as "undeclared" if they are only declared using `G.var_name` or `NS.var_name`.
