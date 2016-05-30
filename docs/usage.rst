..  rudiments documentation: usage

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

Using rudiments
===============


Web Access Helpers
------------------

The :mod:`rudiments.www` module helps with handling web resources.

The context manager :func:`rudiments.www.url_as_file` can be used to make the content
of an URL available as a local file, so it can be fed to things that only work with
local filesystem paths. House-keeping is automatic, so the file is removed on leaving
the context unless you removed or moved it yourself before that.


Security Helpers
----------------

Credentials Lookup
^^^^^^^^^^^^^^^^^^

When using HTTP APIs or other secured web resources, you are confronted with the
question how to enable your users to store their credentials in a
*secure but still convenient* fashion.
The :class:`rudiments.security.Credentials` class tries to give an answer,
by providing some common methods for credential lookup that occupy different
spots in the secure vs. convenient spectrum.
Given a *target* that requires authorization in the form of a username and password or API token,
this class will try several methods to find matching credentials in ‘common’ places.

For URLs (``http``, ``https``, ``ftp``, or ``ftps``), the following steps will be taken:

* The URL's ``user@pwd`` part is checked first.
* Next, the system's `keyring`_ is queried for an entry under the URL's host name.
* Similarly, `~/.netrc` is scanned for matching entries next.
* If nothing can be found, the user is prompted on the console.

As a general fallback, any given target that is not an URL will ask the user
for a username / password pair.

The keyring and netrc are actually queried for two entries,
``user@host`` first and ``host`` second.
This allows the user to easily assume different roles on a target system,
e.g. to access a normal and a privileged account.
The ``user`` value is either taken from the URL,
or else the user's login name is utilized.

To use the class, create a :class:`rudiments.security.Credentials` object,
passing in the *target*. Then to retrieve matching credentials, call the
:func:`rudiments.security.Credentials.auth_pair` method.

.. code-block:: python

    access = Credentials('http://jane@doe.example.com')
    username, password = access.auth_pair()

Note that this allows to only prompt the user for a password when it's actually needed,
but still create the credentials object early on, during some setup phase.


.. _`keyring`: http://pythonhosted.org/keyring/


Humanized Input and Output
--------------------------

For accepting input from prompts and configuration files, and presenting values
in a form easily parsed by humans, the :mod:`rudiments.humanize` module offers
conversion functions for common data types.

For handling byte sizes in `IEC binary units`_, use
:func:`rudiments.humanize.bytes2iec` and :func:`rudiments.humanize.iec2bytes`.
Examples::

    >>> bytes2iec(1536), bytes2iec(10**9)
    (u'   1.5 KiB', u' 953.7 MiB')
    >>> bytes2iec(1536, compact=True)
    u'1.5KiB'
    >>> iec2bytes(1), iec2bytes('64k'), iec2bytes('1.234TiB')
    (1, 65536, 1356797348675)

By default, the formatted values are suited for tabulated output (they're all the same length);
when passing ``compact=True``, you'll get a result that better fits into log messages.

To present lists of numbers in a compact form, collapsing consecutive ranges,
:func:`rudiments.humanize.merge_adjacent` can be used.

    >>> ', '. join(humanize.merge_adjacent(('9', 5, 10, 7) + tuple(range(5))))
    u'0..5, 7, 9..10'


.. _`IEC binary units`: http://physics.nist.gov/cuu/Units/binary.html


Python Runtime Support
----------------------

Use the :mod:`rudiments.pysupport` module to access some helpers which
hide internals of the Python interpreter runtime and provide an easier to use interface.

The functions :func:`rudiments.pysupport.import_name`
and :func:`rudiments.pysupport.load_module`
can be used for dynamic imports and adding a simple plugin system to your application.

To help with keeping code portable between Python 2.7 and 3.x,
the :mod:`rudiments._compat` module offers unified names and semantics
for common features that differ between current and legacy Python versions.
It is based on the module with the same name found in `Jinja2`_.


.. _`Jinja2`: http://jinja.pocoo.org/


Operating System Related Extensions
-----------------------------------

In :mod:`rudiments.system`, you find low-level extensions to stdlib modules like
``os`` and ``sys``.

Constants in this module that start with ``EX_`` are standard exit codes to be used
with ``sys.exit()``, as defined in the C header file ``sysexits.h``.


Extensions to 3rd Party Libraries
---------------------------------

The sub-package :mod:`rudiments.reamed` contains modules that
extend the API of some outside library.

Note that you need to add the underlying package to your dependencies
in addition to rudiments, in case you use one of the modules in that sub-package.
``rudiments`` itself does not publish any dependencies on them.

Where the extended package has a condensed public API (i.e. names are usually
only imported from the package name), these modules can serve as a drop-in
replacement, so you just have to change the import statement a little.


Extensions to Click
-------------------

You can use the :mod:`rudiments.reamed.click` module as a drop-in replacement
for `Click <http://click.pocoo.org/>`_, like this:

.. code-block:: python

    from rudiments.reamed import click

There are additional helper functions: :func:`rudiments.reamed.click.pretty_path`
wraps :func:`rudiments.reamed.click.format_filename` to make a file system path
presentable to humans, especially for logging purposes.
The :func:`rudiments.reamed.click.serror` function prints an already styled, very
visible error message, while using any arguments to format the message.


The :class:`rudiments.reamed.click.LoggedFailure` exception can be used when
you want to abort a command with a clearly visible error – the message is styled
identically to what ``serror()`` produces, white bold text on a red background.


:class:`rudiments.reamed.click.AliasedGroup` allows you to define alias names
for commands you defined via the usual annotatons. Here is an example that maps
the ``ls`` alias to the official ``list`` command name:

.. code-block:: python

    from rudiments.reamed import click

    class SmurfAliases(click.AliasedGroup):
        """Alias mapping for 'smurf' commands."""
        MAP = dict(
            ls='list',
        )


    @cli.group(cls=SmurfAliases)
    def smurf():
        """Management of smurfs."""


    @smurf.command(name='list')
    def smurf_list():
        """A command that lists smurfs."""
        # …


Finally, the biggest addition is a default configuration parsing machinery in
the :class:`rudiments.reamed.click.Configuration` class. It should be instantiated
in your root command, passing in the (optional) name of a specific configuration file,
or a path of such files.

.. code-block:: python

    @click.group()
    @click.option('-c', '--config', "config_paths", metavar='FILE',
                  multiple=True, type=click.Path(), help='Load given configuration file(s).')
    @click.pass_context
    def cli(ctx, config_paths=None):
        """Some command line tool."""
        config.Configuration.from_context(ctx, config_paths)

The prepared configuration object is then available to any sub-command via the context,
as ``ctx.obj.cfg``. For more details, see the :class:`rudiments.reamed.click.Configuration`
documentation.
