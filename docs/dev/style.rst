Style Guide
===========

Code for this project must be developed according to the style guide
below.  This guide is designed to ensure that all functions and
code-paths are well written and that work from multiple developers is
cohesive and easily understood.


Python
------

Python code should be compliant with PEP8 and PEP257.  All functions
must have doc-strings and must have appropriate names that make clear
their purpose.  Python should be wrapped at 80 characters and should
not use external libraries where possible.

Where possible, all Python methods should have unit tests.

All Python is linted by flake8, but automatically generated files are
not scored in calculating if an error is a build-breaker.


JavaScript
----------

Javascript should be well documented and tested manually as no
automatic testing is in place.  JavaScript should be wrapped at 80
characters and should not make use of 'spaghetti' function calls.

JavaScript should lint with ESLint and return no warnings or errors.
