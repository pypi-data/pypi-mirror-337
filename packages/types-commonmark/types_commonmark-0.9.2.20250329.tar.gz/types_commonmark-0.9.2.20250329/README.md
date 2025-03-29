## Typing stubs for commonmark

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`commonmark`](https://github.com/rtfd/commonmark.py) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `commonmark`. This version of
`types-commonmark` aims to provide accurate annotations for
`commonmark==0.9.*`.

`commonmark` is deprecated in favor of [markdown-it-py](https://pypi.org/project/markdown-it-py/).
See [this issue](https://github.com/readthedocs/commonmark.py/issues/308) for background and discussion.

*Note:* `types-commonmark` is unmaintained and won't be updated.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/commonmark`](https://github.com/python/typeshed/tree/main/stubs/commonmark)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.398,
and pytype 2024.10.11.
It was generated from typeshed commit
[`43385c455ffbec0ad90deb4d1acc8a1f30eb47c0`](https://github.com/python/typeshed/commit/43385c455ffbec0ad90deb4d1acc8a1f30eb47c0).