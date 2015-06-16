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
