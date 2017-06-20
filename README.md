# Rudiments

![logo](https://raw.githubusercontent.com/jhermann/rudiments/master/docs/img/logo.png)  | Fundamental elements for any Python project, like configuration handling.
:----: | :----
**Project** | [![Librelist](https://img.shields.io/badge/Librelist-python.rudiments-orange.svg)](http://librelist.com/browser/python.rudiments) [![Documentation](https://readthedocs.org/projects/rudiments/badge/?version=latest)](https://readthedocs.org/projects/rudiments/?badge=latest) [![License](https://img.shields.io/pypi/l/rudiments.svg)](https://github.com/jhermann/rudiments/blob/master/LICENSE)
**QA** | [![Travis CI](https://api.travis-ci.org/jhermann/rudiments.svg)](https://travis-ci.org/jhermann/rudiments) [![Coveralls](https://img.shields.io/coveralls/jhermann/rudiments.svg)](https://coveralls.io/r/jhermann/rudiments) [![GitHub Issues](https://img.shields.io/github/issues/jhermann/rudiments.svg)](https://github.com/jhermann/rudiments/issues)
**Release** | [![Latest Version](https://img.shields.io/pypi/v/rudiments.svg)](https://pypi.python.org/pypi/rudiments/) [![Downloads](https://img.shields.io/pypi/dw/rudiments.svg)](https://pypi.python.org/pypi/rudiments/)


## Overview

This library collects ‘miscellaneous’ functionality that is unspecific in nature and shared among many projects.
It also collects small extensions to other support packages that don't warrant their own project,
in the ``rudiments.reamed`` package.

See “Other Packages” below for problem domains that are already covered by good to excellent solutions.

:speech_balloon: | To get help or talk about this project, please use the python.rudiments@librelist.com mailing list.
---- | :----


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
[Arrow](https://arrow.readthedocs.io/) | Better dates and times for Python – see also [Pendulum](https://github.com/sdispater/pendulum), [Delorean](https://github.com/myusuf3/delorean), and [Maya](https://github.com/kennethreitz/maya)
[boltons](https://boltons.readthedocs.io/en/latest/) | A set of pure-Python utilities augmenting the stdlib
[Click](http://click.pocoo.org/) | Command line interface framework
[colorama](https://pypi.python.org/pypi/colorama) | Cross-platform colored terminal text
[github3.py](http://github3py.readthedocs.io/) | GitHub API v3 client
[netifaces](https://bitbucket.org/al45tair/netifaces) | Portable network interface information
[pyparsing](https://pyparsing.wikispaces.com/) | A library of classes that allows to construct a grammar in pure Python code
[poyo](https://github.com/hackebrot/poyo) | A pure-Python YAML parser
[Requests](http://docs.python-requests.org/en/latest/) | Anything HTTP
[Reusables](https://github.com/cdgriffith/Reusables) | Utilities that programmers may find themselves often recreating
[sh](http://amoffat.github.io/sh/) | Full-fledged subprocess interface, treat any program as if it were a function
[sorted_containers](https://github.com/grantjenks/sorted_containers) | Ordered collections (list, dict, set), pure Python and as fast as C
[Soupy](http://soupy.readthedocs.io/) | Soupy wraps a fluent query interface around BeautifulSoup.

Specifically on the subject of configuration handling, these are the ones to consider…

Project | Description
----: | :----
[configobj](http://configobj.readthedocs.io/en/latest/) | Config file reading, writing and validation
[dectate](https://github.com/morepath/dectate) | A powerful configuration engine for Python frameworks, based on decorators.
[dynaconf](https://github.com/rochacbruno/dynaconf) | OSM (Object Settings Mapper) reading from a set of different data stores such as Python settings files, environment variables, Redis, Memcached, INI files, JSON files, YAML files, or your custom extension
[configman](https://github.com/mozilla/configman) | The grand unified configuration system from Mozilla
[prettyconf](https://github.com/osantana/prettyconf) | Easy separation of configuration and code, following the recomendations for 12 Factor apps
[biome](https://github.com/darvid/biome) | Provides painless typed access to namespaced environment variables

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

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See [CONTRIBUTING](https://github.com/jhermann/rudiments/blob/master/CONTRIBUTING.md) for more.


## References

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.io/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.io/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [Rituals](https://jhermann.github.io/rituals)
* [keyring](http://pythonhosted.org/keyring/)


## Acknowledgements

* Documentation hosted by [Read the Docs](https://readthedocs.org/).
