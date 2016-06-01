..  rudiments documentation: end-user

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

End-User Documentation
======================

*This chapter contains instructions targeted at users of projects that are using this library, so that you can link to thse from your onw documentation.*

.. _auth-credentials:

Configuration of Authentication Credentials
-------------------------------------------

When using HTTP APIs or other secured web resources, you usually want to
store your credentials in a *secure but still convenient* fashion.
Given a *target* that requires authentication in the form of a username and password or API token,
the application will try several methods to find matching credentials in ‘common’ places.

For URLs (``http``, ``https``, ``ftp``, or ``ftps``), the following steps will be taken:

* The URL's ``user@pwd`` part is checked first and used if present.
* Next, the system's `keyring`_ is queried for an entry under the URL's host name.
* Similarly, ``~/.netrc`` is scanned for matching entries next.
* If nothing can be found, you will be prompted on the console.

As a general fallback, any given target that is not an URL will ask for a username / password pair.

The keyring and netrc file are actually queried for two entries,
``user@host`` first and ``host`` second.
This allows you to easily assume different roles on a target system,
e.g. to access a normal and a privileged account.
The ``user`` value is either taken from the URL,
or else your login name is utilized — so for an admin account,
use something like ``https://admin@service.example.com/``
and a matching password entry for ``admin@example.com``.


Installation Procedures
^^^^^^^^^^^^^^^^^^^^^^^

For using netrc files and prompting, nothing extra has to be installed,
because Python has everything needed on board.
By using `keyring`_ credentials, you gain more security (stored passwords are
encrypted and only available after you logged in to your account), at the
possible price of installing additional software.
Consult the manual of your application whether any of the following
installation steps are actually necessary and suitable — at least the
``keyring`` Python package will normally be included when you install
an application.

On *Windows* and *Mac OS X*, you don't need to install extra system software,
but on a *Linux* system the OS package necessary for installing the ``dbus-python``
Python package has to be made available. On Debian-type systems, that means
calling this command:

.. code-block:: shell

    sudo apt-get install libdbus-glib-1-dev python-dev libffi-dev build-essential

For the Python packages, use ``pip`` as follows:

.. code-block:: shell

    pip install secretstorage dbus-python keyring

For *Windows* and *Mac OS X*, only ``keyring`` is needed.
To test that you installed all supporting libraries in a *Linux* setup, try this:

.. code-block:: shell

    $ python -c "import keyring; print keyring.get_keyring()"
    <keyring.backends.SecretService.Keyring object at 0x7f091526bcd0>

If it doesn't work or the essential components are not installed,
in the output you'll get ``keyring.backends.fail.Keyring`` instead.
A successful installation on other operating systems will show
some different back-end that is not the ‘fail’ one.

On a *Gnome* desktop (e.g. *Ubuntu 14.04* and up), the end-user application
to manage passwords is ``seahorse`` a/k/a “Passwords and Keys”.
It can be used to check that your passwords are stored correctly,
and to change and delete them.


.. _`keyring`: http://pythonhosted.org/keyring/
