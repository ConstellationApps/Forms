Development Roadmap
===================

As the forms system is a large and complex body of code, this project
is split up into several phases.  There are outlined below:


Phase I - Milestone 0.1.0
-------------------------

This phase is focused on the main components of a forms sytem which
are related to the functions a user expects in creating, filling out,
and viewing a form.  This phase also includes the tasks related to
setting up the required project infrastructure and setting up the
Python package schema for the project.  Goals for this phase of the
project include:

* Build infrastructure

  * PRs are checked using Travis CI according to the Style Guide
  * Create and verify the Python Egg structure

* Documentation

  * Sphinx documentation base is in place
  * Continuous documentation builds are in place

* Forms System

  * Forms can be created
  * Forms can be edited
  * Forms can be filled out
  * Forms can be submitted
  * Completed forms can be viewed
  * Completed forms can be exported


.. warning:: Version 0.1.0 remains unreleased as an internal alpha
             version due to complications with the rest of the
             Constellation Suite.
    
Phase II - Milestone 0.2.0
--------------------------

This phase includes the more advanced features such as being able to
comment on and make notes on submitted forms.  This supports use cases
where the person reviewing the form needs to ask for changes from the
person who is submitting the form.  Ultimately this will be a fairly
simple feature, but will require a fairly large amount of code to
implement.  Goals for this phase include:

* Documentation

  * Initial user documentation will be created
  * Complete documentation for the submitted forms export API

* Forms System

  * Possible to upload form attachments
  * Possible to review and comment on forms

    * Comments can be visible to the submitter or private
    * Reviews can either be approved, or denied
    * Form submitters can see previous forms and statuses
