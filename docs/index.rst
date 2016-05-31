..  rudiments documentation master file

    Copyright ©  2015 Jürgen Hermann <jh@web.de>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Welcome to the “Rudiments” manual!
==================================

.. image:: img/logo.png

*Rudiments* is a Python library that offers ‘miscellaneous’ functionality which
is unspecific in nature and shared among many projects. It also collects small
extensions to other support packages that don't warrant their own project,
in the :mod:`rudiments.reamed` package.


Important Links
---------------

  * `GitHub Project <https://github.com/jhermann/rudiments>`_
  * `Issue Tracker <https://github.com/jhermann/rudiments/issues>`_
  * `PyPI <https://pypi.python.org/pypi/rudiments/>`_
  * `Latest Documentation <https://rudiments.readthedocs.org/en/latest/>`_
  * `Mailing List <http://librelist.com/browser/python.rudiments/>`_


Installing
----------

*Rudiments* can be installed from PyPI via ``pip install rudiments`` as
usual, see `releases <https://github.com/jhermann/rudiments/releases>`_
on GitHub for an overview of available versions – the project uses
`semantic versioning <http://semver.org/>`_ and follows
`PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_ conventions.
To get a bleeding-edge version from source, use these commands:

.. code-block:: shell

    repo="jhermann/rudiments"
    pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
    pip install -UI -e "git+https://github.com/$repo.git#egg=${repo#*/}"

See the following section on how to create a full development environment.



Contributing
------------

To create a working directory for this project, call these commands:

.. code-block:: shell

    git clone "https://github.com/jhermann/rudiments.git"
    cd "rudiments"
    . .env --yes --develop
    invoke build --docs test check

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See :doc:`CONTRIBUTING` for more.


Documentation Contents
----------------------

.. toctree::
    :maxdepth: 4

    usage
    end-user
    fullapi
    CONTRIBUTING
    LICENSE


References
----------

Tools
^^^^^

-  `Cookiecutter <http://cookiecutter.readthedocs.org/en/latest/>`_
-  `PyInvoke <http://www.pyinvoke.org/>`_
-  `pytest <http://pytest.org/latest/contents.html>`_
-  `tox <https://tox.readthedocs.org/en/latest/>`_
-  `Pylint <http://docs.pylint.org/>`_
-  `twine <https://github.com/pypa/twine#twine>`_
-  `bpython <http://docs.bpython-interpreter.org/>`_
-  `yolk3k <https://github.com/myint/yolk#yolk>`_

Packages
^^^^^^^^

-  `Rituals <https://jhermann.github.io/rituals>`_


Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
