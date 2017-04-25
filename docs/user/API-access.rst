API Access
==========

While the Constellation Forms module is designed to conduct all form
review tasks internally, it is often desireable to export data from
the system for use in other systems.  For situations where this is
necessary, API access is provided.  To use the API, your Systems
Administrator will need to add an API Key (:ref:`api-key-access`).

To make a request to the API, send your API key as the
:code:`X-AUTHORIZATION` header.  An example is shown below.

.. code-block:: bash

   % curl https://127.0.0.1:8000/forms/api/export/1 --header \
   "X-AUTHORIZATION:MySecureKey"
   id,Username
   0123456789,test

In the example above, the request is sent for the :code:`id` and
:code:`username` fields of form ID 1.  These field names are the field
names of the individual form fields.  The API endpoint takes the form
of:

.. code-block:: bash

   https://<constellation_address>/forms/api/export/<form_id>

In the previous example, :code:`MySecureKey` is the API key.

.. note:: It is not necessary to use curl to query the API.
