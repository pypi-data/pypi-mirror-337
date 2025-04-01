## Typing stubs for greenlet

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`greenlet`](https://github.com/python-greenlet/greenlet) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `greenlet`. This version of
`types-greenlet` aims to provide accurate annotations for
`greenlet==3.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/greenlet`](https://github.com/python/typeshed/tree/main/stubs/greenlet)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.398,
and pytype 2024.10.11.
It was generated from typeshed commit
[`bfd032156c59bbf851f62174014f24f4f89b96af`](https://github.com/python/typeshed/commit/bfd032156c59bbf851f62174014f24f4f89b96af).