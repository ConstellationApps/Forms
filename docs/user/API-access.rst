API Access
==========

.. warning:: This feature is designed for advanced users only.  If you
             require API access, you may wish to consult with a
             qualified developer to connect your application to the
             Constellation Forms API.

While the Constellation Forms module is designed to conduct all form
review tasks internally, it is often desireable to export data from
the system for use in other systems.  For situations where this is
necessary, API access is provided.  To use the API, your Systems
Administrator will need to add an API Key (:ref:`api-key-access`).

To make a request to the API, send your API key as the
:code:`X-AUTHORIZATION` header.  An example is shown below.

.. code-block:: bash

   % curl https://127.0.0.1:8000/forms/api/export/1 --header \
   "X-AUTHORIZATION:admin MySecureKey"
   id,Username
   0123456789,test

In the example above, the request is sent with no filters so the all
fields are returned (in this case they are called :code:`id` and
:code:`username`).  These field names are the field names of the
individual form fields.  The API endpoint takes the form of:

.. code-block:: bash

   https://<constellation_address>/forms/api/export/<form_id>

In the previous example, :code:`MySecureKey` is the API key which
belongs to the :code:`admin` user.

.. note:: It is not necessary to use curl to query the API.
