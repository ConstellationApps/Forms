Configuration
=============

The Constellation Forms module offers very few configurable parameters
at the module level.  With the exception of assigning permissions to
groups that are permitted to create forms, no other values are
provided for configuration.  API keys must be created by a staff user
if an unpriviledged user requires API access.


Create Form Permission
----------------------

To grant a user the ability to create a form, select the group that
contains the user and assign that group the
:code:`constellation_forms|form|Can add form` permission.  This
permission grants the user the ability to create new forms.  Once
created, all permissions for particular form objects are assigned to
the owning group for that form.  In the event that a user needs to
change what group has access to update, alter, or process submissions
for a form the form group ownership will need to be changed.

At this time it is not supported to grant ownership on a form to a
single user.


.. _api-key-access:

API Keys
--------

In some cases users may require programatic access to retrieve form
data.  To secure such access, Constellation Forms makes use of API
keys.  These keys must be created by a user holding either the Django
Staff or Superuser rank.

To create a new API key:

1. :menuselection:`Django adminsitration --> constellation_forms -->
API keys`.

2. Select which user this key is for and paste in the key text.  Each
user may hold one and only one key at a time.

Updates to the key value take effect instantly on submitting the form.
For maximum flexibility, the key value may be any string that can be
encoded in an HTTP header.  In general, this can be any alphanumeric
sequence of characters.  While the keys can be any length, it is not
recommended to use keys longer than 255 characters for performance
reasons.
