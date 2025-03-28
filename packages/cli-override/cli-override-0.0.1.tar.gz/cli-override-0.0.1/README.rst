------------
Cli Override
------------

..
  .. image:: https://img.shields.io/pypi/v/cli-override
      :target: https://pypi.org/project/cli-override/
      :alt: PyPI Version

..
  .. image:: https://github.com/blester125/cli-override/workflows/Unit%20Test/badge.svg
      :target: https://github.com/blester125/cli-override/actions
      :alt: Actions Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

..
  .. image:: https://readthedocs.org/projects/cli-override/badge/?version=latest
      :target: https://cli-override.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status


This library lets you pass arbitrary over arguments from the cli like so::

  from cli_override import parse_extra_args

  args, unknown_args = parser.parse_known_args()
  extra_args = parse_extra_args(unknown_args)

  my_override_value = extra_args.get["my_override_flag"]

Invocation of your program with::

  python my_script.py --x:my_override_flag 14

results in `my_override_value` being `14`.
