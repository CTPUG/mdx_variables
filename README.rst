mdx_variables
=============

|variables-ci-badge|

.. |variables-ci-badge| image:: https://github.com/CTPUG/mdx_variables/actions/workflows/tests.yml/badge.svg
    :alt: GitHub Actions CI status
    :scale: 100%
    :target: https://github.com/CTPUG/mdx_variables/actions/workflows/tests.yml

A Markdown extension to add support for variables.

Licensed under the `ISC License`_.

.. _ISC License: https://github.com/CTPUG/mdx_variables/blob/master/LICENSE


Requirements
============

The mdx_variables plugin requires only the base `markdown`_ library.

.. _markdown: http://pythonhosted.org/Markdown/


Installation
============

Install with ``pip install mdx_variables``.


Documentation
=============

Allows inserting variables into Markdown.

The following Markdown example:

.. code:: markdown

  This paragraph contains ${chickens} chickens.

  This paragraph contains no chickens but ${foxes} foxes.

  Are there ninjas here? ${ninjas}.

Might result in:

.. code:: markdown

  This paragraph contains 5 chickens.

  This paragraph contains no chickens but 3 foxes.

  Are there ninjas here? ninjas not found.


Python usage:

.. code:: python

  md = markdown.Markdown(
      extensions=[
          'variables',
      ],
      extension_configs={
          'variables': {
              'vars': {
                'chickens': '5',
                'foxes': (lambda: 3),
                '__getattr__': (lambda name: "{} not found".format(name)),
              },
          }
      })

Configuration options:

* ``vars``: A dictionary mapping variable names to variable values.

  If a value is a function, that function will be called without arguments and
  the result will be used as the variable value.

  The special variable ``__getattr__`` may specify a function
  ``f(name) -> value`` to call when no matching variable is found.
