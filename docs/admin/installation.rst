Installing the Module
=====================

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
document and is fully unsupported by the Constellation Developers,
however a similar method is used as part of the development process.



Enabling the Module
===================

Once you have installed Constellation Forms by one of the three
mechanisms above, it is necessary to enable it in your Django
installation.  To do so add :code:`constellation_forms` and
:code:`django_guardian` to your :code:`INSTALLED_APPS` variable in
your config file.

The section should look something like this:

.. code-block:: python

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'guardian',
       'constellation_base',
       'constellation_forms',
   ]


Additionally, you will need to add the Guardian backend to the
:code:`AUTHENTICATION_BACKENDS` section of your configuration file.
The section should look like this:

.. code-block:: python

   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.ModelBackend',  # this is default
       'guardian.backends.ObjectPermissionBackend',
   )


Once you've enabled the module in your settings file, the last thing
to do is to mount the module's routes to a URL within your Django
installation.  The is covered in detail in the Django documentation,
but the minimum lines necessary in your root :code:`urls.py` file are
as follows:

.. code-block:: python

   from django.conf import settings
   from django.conf.urls import url, include
   from django.conf.urls.static import static
   from django.contrib import admin

   urlpatterns = [
       url(r'^admin/', admin.site.urls),
       url(r'', include('constellation_base.urls')),
       url(r'forms/', include('constellation_forms.urls')),
   ]

Now that you've got your Django installation setup, you can apply the
migrations for Constellation Forms and Guardian, onboard your users,
and be on your way to creating all the forms you could desire!
