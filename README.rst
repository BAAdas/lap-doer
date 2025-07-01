Lap-Doer
========

Lap-Doer is an open-source automotive lap simulation framework developed to support performance analysis, vehicle modeling, and track dynamics. It is actively developed within a Formula Student team to support both design validation and race strategy development. The framework is grounded in real-world data and academic references, with an initial focus on steady-state simulation. Lap-Doer aims to evolve into a comprehensive transient simulation platform.

Join our community on `Discord <https://discord.gg/r4JzG2HXqT>`_.

Setup
-----

Install dependencies:

.. code-block:: bash

    poetry install

Enable pre-commit hooks for clean commits:

.. code-block:: bash

    poetry run pre-commit install

Development
-----------

Lap-Doer uses `Poetry <https://python-poetry.org/>`_ for dependency management, `Pytest <https://docs.pytest.org/>`_ for testing, and `Ruff <https://docs.astral.sh/ruff/>`_ for linting and code style enforcement.

Run tests:

.. code-block:: bash

    poetry run pytest

Lint code:

.. code-block:: bash

    poetry run ruff check --fix .

Format code:

.. code-block:: bash

    poetry run ruff format .

Contributing
------------

Contributions are welcome! Please open issues for bugs or feature requests, and feel free to submit pull requests.

License
-------

Specify your license here (e.g., MIT, Apache 2.0).

