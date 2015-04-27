# Rudiments

Fundamental elements for any Python project, like configuration handling.

 [![Travis CI](https://api.travis-ci.org/jhermann/rudiments.svg)](https://travis-ci.org/jhermann/rudiments)
 [![Coveralls](https://img.shields.io/coveralls/jhermann/rudiments.svg)](https://coveralls.io/r/jhermann/rudiments)
 [![GitHub Issues](https://img.shields.io/github/issues/jhermann/rudiments.svg)](https://github.com/jhermann/rudiments/issues)
 [![License](https://img.shields.io/pypi/l/rudiments.svg)](https://github.com/jhermann/rudiments/blob/master/LICENSE)
 [![Development Status](https://pypip.in/status/rudiments/badge.svg)](https://pypi.python.org/pypi/rudiments/)
 [![Latest Version](https://img.shields.io/pypi/v/rudiments.svg)](https://pypi.python.org/pypi/rudiments/)
 [![Download format](https://pypip.in/format/rudiments/badge.svg)](https://pypi.python.org/pypi/rudiments/)
 [![Downloads](https://img.shields.io/pypi/dw/rudiments.svg)](https://pypi.python.org/pypi/rudiments/)


## Overview

This library collects ‘miscellaneous’ functionality that is unspecific in nature and shared among many projects.
It also collects small extensions to other support packages that don't warrant their own project,
in the ``rudiments.reamed`` package.

See “Other Packages” below for problem domains that are already covered by good to excellent solutions.


## Usage

*Rudiments* can be installed from PyPI via ``pip install rudiments`` as usual,
see [releases](https://github.com/jhermann/rudiments/releases) for an overview of available versions
– the project uses [semantic versioning](http://semver.org/)
and follows [PEP 440](https://www.python.org/dev/peps/pep-0440/) conventions.
To get a bleeding-edge version from source, use these commands:

```sh
repo="jhermann/rudiments"
pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
pip install -UI -e "git+https://github.com/$repo.git#egg=${repo#*/}"
```

See [Contributing](#contributing) on how to create a full development environment.


## Other Packages

This is a list of packages that solve a certain problem domain
and are (hopefully) best-of-breed.

Project | Description
----: | :----
[Arrow](https://arrow.readthedocs.org/) | Better dates and times for Python
[boltons](https://boltons.readthedocs.org/en/latest/) | A set of pure-Python utilities augmenting the stdlib
[Click](http://click.pocoo.org/) | Command line interface framework
[colorama](https://pypi.python.org/pypi/colorama) | Cross-platform colored terminal text
[configobj](http://configobj.readthedocs.org/en/latest/) | Config file reading, writing and validation
[github3.py](http://github3py.readthedocs.org/) | GitHub API v3 client
[pyparsing](https://pyparsing.wikispaces.com/) | A library of classes that allows to construct a grammar in pure Python code
[Requests](http://docs.python-requests.org/en/latest/) | Anything HTTP
[sh](http://amoffat.github.io/sh/) | Full-fledged subprocess interface, treat any program as if it were a function
[Soupy](http://soupy.readthedocs.org/) | Soupy wraps a fluent query interface around BeautifulSoup.

The following help you with writing your unit and integration tests.

Project | Description
----: | :----
[pytest-localserver](https://pypi.python.org/pypi/pytest-localserver) | *py.test* plugin to test server connections locally
[Responses](https://github.com/getsentry/responses) | A utility for mocking out the *Requests* library


## Contributing

To create a working directory for this project, call these commands:

```sh
git clone "https://github.com/jhermann/rudiments.git"
cd "rudiments"
. .env --yes --develop
invoke build --docs test check
```

See [CONTRIBUTING](https://github.com/jhermann/rudiments/blob/master/CONTRIBUTING.md) for more.


## References

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.org/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [Rituals](https://jhermann.github.io/rituals)


## Acknowledgements

…
