Installation
============

There are two ways to install the Constellation Forms application.
The easy and recommended way is to use Python Pip.  If you have some
compelling reason to not install with the Python package mechanisms,
you can install from source.  This is not recommended and is
unsupported by the Constellation release team.


The Easy Way
------------

To install from pip, install the `Constellation-Forms` package.  This
package is only available for Python3 at this time.  The
Constellation-Forms package depends on Constellation-Base, Django, and
psycopg2.  If you do not have these installed they will be installed
as depedencies of the Constellation-Forms.


The Slightly Difficult Way
--------------------------

If you cannot use pip in an online mode, but still have the tools
available to you (i.e. you have a firewall that does not permit
connections to pypi.python.org) then you can manually download the
wheels and install them by hand.  To do this navigate to the
`Constellation Forms PyPI page
<https://pypi.python.org/pypi/Constellation-Forms/>`_, and download
the \*.whl file for the current release.  Additionally download the
wheels for Django, Django-Guardian, Psycopg2, and the dependencies of
the Constellation-Base software.

To install the wheels, use :code:`pip install <wheel>`.  After you have
installed Constellation Forms, you can enable the module as though it
had been installed by pip.


The Hard Way
------------

If there is a compelling reason to not use Python pip it is possible
to download the distribution tarballs from GitHub and decompress them
manually.  This installation mechanism is beyond the scope of this
document and is fully unsupported by the Constellation Developers.
