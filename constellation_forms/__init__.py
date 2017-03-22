"""
This module implements a forms system for creating, filling out, and
reviewing forms within an organization.  This module depends on the
Constellation-Base package to function correctly.

Constellation Forms implements a fairly standard forms system.  The
core features include:

* Click-to-Build form builder
* Form Lifecycles
* Form Versions

More advanced features such as form approval status are planned.  This
will allow for advanced tracking of forms used for internal processes
such as purchase approvals, access requests, and even appeals to
normal form processes.

This documentation is designed to be read by two distinct groups.  The
primary group consuming this documentation are the developers of the
Forms module.  While most of the source code is documented and the
files contain extensive inline comments, this documentation serves to
provide more in depth discussions of key features of components.  This
also provides information on core design choices and why certain
choices have been made.

The second group of people expected to read
this documentation are end users of the system who would like to know
how to use components.  This includes people who are managing the
forms system, and people who are tasked with creating forms.
"""
