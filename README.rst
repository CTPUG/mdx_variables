mdx_variables
=============

|variables-ci-badge|

.. |variables-ci-badge| image:: https://travis-ci.org/CTPUG/mdx_variables.png?branch=master
    :alt: Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/CTPUG/mdx_variables

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

Markdown example:

.. code:: markdown

  This paragraph contains ${chickens} chickens.

  This paragraph contains no chickens.

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
