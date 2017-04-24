System Architecture
===================

The forms system follows the main Constellation Application module
architecture.  There are 2 key components of this architecture that
are mentioned here:

  * Authentication/Authorization: All authentication is deferred to
    the main Constellation login page and any authorization is
    deferred to Django-Guardian system for per-object permissions.
    The per object permissions are needed to ensure that each form can
    have seperate permissions and seperate controls for access.
  * The Forms module must not modify any componenets at the system
    level or tamper with any platform level values.

The Forms module adds a dependency on PostgreSQL that is not held by
other modules of the Constellation Suite.  This allows the use of the
JSONb type for storing the forms and form data.  While using a NoSQL
approach would normally be slow and come with caveats for indexing, we
use a combination where the indexes are created on normal SQL fields
and the data stored in the JSONb field is only ever retrieved or
written in full.  It is possible to downgrade this model to use a
TextField string instead, but as PostgreSQL is the preferred database
management system (DBMS) for production Constellation installations,
no alternate storage backends are implemented at this time.

For an in depth discussion of the data models used by the forms
application, please consule the :doc:`models/index` documentation.
