# Pylint Check Reference

Detailed explanations and fix suggestions for each pylint check used in this skill.

## Error Checks

### syntax-error
**Description**: The code contains invalid Python syntax that prevents parsing.
**Example**: `if x = 5:`
**Fix**: Correct the syntax. Use `==` for comparison: `if x == 5:`

### undefined-variable
**Description**: A variable is used before being defined.
**Example**: `print(x)` (where `x` was never defined)
**Fix**: Define the variable before use or check for typos.

### no-member
**Description**: An object doesn't have the requested attribute or method.
**Example**: `"hello".append("x")`
**Fix**: Check the object type and use correct attributes/methods.

### not-callable
**Description**: An object is being called as a function but isn't callable.
**Example**: `result = my_dict()`
**Fix**: Remove parentheses or use a callable object.

### used-before-assignment
**Description**: A variable is used before it's assigned in all code paths.
**Example**:
```python
if condition:
    x = 5
print(x)  # Error if condition is False
```
**Fix**: Ensure variable is assigned in all code paths.

### possibly-used-before-assignment
**Description**: A variable might be used before assignment in some conditions.
**Fix**: Initialize variable before conditional blocks.

### unsubscriptable-object
**Description**: An object that can't be indexed is being subscripted.
**Example**: `x = 5; y = x[0]`
**Fix**: Use a subscriptable type (list, dict, tuple, string).

### bad-file-encoding
**Description**: File has encoding issues (usually non-UTF-8 without encoding declaration).
**Fix**: Add `# coding: utf-8` at the top or save as UTF-8.

### duplicate-key
**Description**: A dictionary has duplicate keys.
**Example**: `{"a": 1, "a": 2}`
**Fix**: Remove duplicate keys.

### reimported
**Description**: A module is imported multiple times.
**Example**:
```python
import os
from sys import os
```
**Fix**: Remove duplicate imports.

### redefined-builtin
**Description**: A built-in function name is reused.
**Example**: `list = [1, 2, 3]`
**Fix**: Use different variable names (e.g., `my_list`).

### redefined-outer-name
**Description**: An outer scope variable name is reused in an inner scope.
**Fix**: Use different names to avoid shadowing.

### function-redefined
**Description**: A function is defined multiple times.
**Fix**: Remove duplicate definitions or rename.

### expression-not-assigned
**Description**: A value is computed but not assigned to anything.
**Example**: `len([1, 2, 3])` as a standalone line.
**Fix**: Assign to variable or remove if not needed.

### unreachable
**Description**: Code exists that can never be executed.
**Example**: Code after `return` or `raise`.
**Fix**: Remove unreachable code.

## Convention Checks

### missing-final-newline
**Description**: File doesn't end with a newline.
**Fix**: Add a blank line at the end of the file.

### bad-indentation
**Description**: Inconsistent indentation (mixing tabs and spaces or wrong levels).
**Fix**: Use consistent indentation (4 spaces per level recommended).

### trailing-whitespace
**Description**: Lines have trailing whitespace.
**Fix**: Remove trailing spaces/tabs.

### line-too-long
**Description**: Line exceeds maximum length (default: 100 characters).
**Fix**: Break long lines into multiple lines.

### superfluous-parens
**Description**: Unnecessary parentheses.
**Example**: `if (x == 5):`
**Fix**: Remove unnecessary parentheses: `if x == 5:`

### redundant-u-string-prefix
**Description**: `u` prefix on strings is redundant in Python 3.
**Example**: `u"hello"`
**Fix**: Use `"hello"` without prefix.

### multiple-statements
**Description**: Multiple statements on same line.
**Example**: `x = 5; y = 10`
**Fix**: Put each statement on its own line.

### unnecessary-pass
**Description**: `pass` statement is unnecessary.
**Example**: `pass` at the end of a function with other code.
**Fix**: Remove the `pass` statement.

## Refactor Checks

### super-with-arguments
**Description**: Using `super()` with arguments in Python 3.
**Example**: `super(Child, self).__init__()`
**Fix**: Use `super().__init__()` without arguments.

### consider-using-generator
**Description**: List comprehension used where generator would be more efficient.
**Example**: `any([x > 0 for x in items])`
**Fix**: Use generator: `any(x > 0 for x in items)`

### consider-using-set-comprehension
**Description**: Creating a set via dict comprehension or loop.
**Fix**: Use set comprehension: `{x for x in items}`

### consider-using-dict-items
**Description**: Iterating over dict keys then accessing values.
**Example**: `for k in d: print(d[k])`
**Fix**: Use items: `for k, v in d.items():`

### consider-using-in
**Description**: Using multiple equality checks.
**Example**: `x == 1 or x == 2 or x == 3`
**Fix**: Use `in`: `x in {1, 2, 3}`

### consider-using-ternary
**Description**: If-else that could be ternary expression.
**Example**:
```python
if condition:
    x = 1
else:
    x = 2
```
**Fix**: Use ternary: `x = 1 if condition else 2`

### simplifiable-if-expression
**Description**: If statement that can be simplified.
**Example**: `if x: return True else: return False`
**Fix**: `return bool(x)` or `return x`

### consider-using-with
**Description**: File/resource not using context manager.
**Example**:
```python
f = open("file.txt")
content = f.read()
f.close()
```
**Fix**: Use context manager:
```python
with open("file.txt") as f:
    content = f.read()
```

### use-a-generator
**Description**: List used where generator expression would be appropriate.
**Fix**: Replace `[]` with `()` for generator.

### unnecessary-comprehension
**Description**: Comprehension that wraps a single value.
**Example**: `[x for x in [1, 2, 3]]`
**Fix**: Use the value directly: `[1, 2, 3]`

### useless-return
**Description**: Return statement at end of function with no value.
**Example**: `return` at end when function returns None anyway.
**Fix**: Remove the return statement.

### useless-parent-delegation
**Description**: Method that just calls parent with same arguments.
**Fix**: Remove the method if it only delegates to parent.

### self-assigning-variable
**Description**: Variable assigned to itself.
**Example**: `x = x`
**Fix**: Remove the assignment or fix typo.

### chained-comparison
**Description**: Comparison that can be chained.
**Example**: `x < 5 and x > 0`
**Fix**: Use chaining: `0 < x < 5`

### singleton-comparison
**Description**: Comparing to singleton with `==`.
**Example**: `x == None` or `x == True`
**Fix**: Use `is`: `x is None` or `x is True`

### f-string-without-interpolation
**Description**: f-string used without any interpolation.
**Example**: `f"hello world"`
**Fix**: Use regular string: `"hello world"`

## Warning Checks

### unused-import
**Description**: Imported module or name is never used.
**Fix**: Remove unused imports.

### unused-argument
**Description**: Function argument is never used.
**Fix**: Use the argument, prefix with `_`, or remove.

### raise-missing-from
**Description**: Raising exception while handling another without `from`.
**Example**:
```python
try:
    ...
except ValueError as e:
    raise TypeError("message")
```
**Fix**: Add cause: `raise TypeError("message") from e`

### no-else-return
**Description**: `else` clause with `return` in `if` block.
**Example**:
```python
if x:
    return 1
else:
    return 2
```
**Fix**: Remove else:
```python
if x:
    return 1
return 2
```

### no-else-raise
**Description**: `else` clause with `raise` in `if` block.
**Fix**: Similar to no-else-return, remove the else.

### use-implicit-booleaness-not-len
**Description**: Checking `len(x) == 0` or `len(x) > 0`.
**Example**: `if len(items) == 0:`
**Fix**: Use implicit booleaness: `if not items:` or `if items:`

### pointless-string-statement
**Description**: String literal as statement (often meant to be docstring).
**Example**: `"This is a string"` at module level.
**Fix**: Make it a docstring or assign to variable.

### pointless-statement
**Description**: Statement that has no effect.
**Example**: `42` as a standalone line.
**Fix**: Remove the statement.

### inconsistent-return-statements
**Description**: Function returns both explicit values and implicitly returns None.
**Example**: Some paths `return x`, others have no return.
**Fix**: Ensure all paths return explicitly or consistently.

### too-many-nested-blocks
**Description**: Too many levels of nested blocks (usually >5).
**Fix**: Extract nested logic into separate functions.

### unidiomatic-typecheck
**Description**: Using `type()` for type checking.
**Example**: `type(x) == list`
**Fix**: Use `isinstance(x, list)`
