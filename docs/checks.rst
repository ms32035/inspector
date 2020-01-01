Checks and check runs
=====================

The concept of a check comes from mathematical equations,
which have a right hand side and a left hand side.
Additionally, a warning value can be set. It is evaluated only
when the primary condition is not met. Warning value was designed
to be used for 'known issues', where a certain degree of discrepancy
is acceptable.

Tagging
-------

:code:`django-taggit` is uses to assign tags to checks. This next allows
to execute all checks with the same tag at once. If you want to run all check,
assign a shared tag i.e. :code:`all` to all checks
