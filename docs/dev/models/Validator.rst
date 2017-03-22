Validators
==========

Validators provide a way to constrain input to a particular format.
Usually this is for saying things like "this box is for a telephone
number, only accept things that look like telephone numbers".  For
simplicity and some degree of portability, we have chosen to implement
the validators as simple Regular Expressions.  This means that
validators aren't exactly easy to edit and define for non-technical
individuals, but they are quick and easy to implement.


.. autoclass:: constellation_forms.models.validator.Validator
   :members:
   :special-members:
