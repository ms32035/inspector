Checks and check runs
=====================

Inspector is built around **checks**.
The concept of comes from mathematical equations that
feature a right-hand side and a left -and side.
Additionally, a warning value can be set to evaluate
when the primary condition is not met. Warning value is intended
to be used for 'known issues', where a certain degree of discrepancy
is acceptable.

Tagging
-------

Inspector uses :code:`django-taggit` for tagging checks. This allows
allows grouping checks according to business needs, and next executing
groups of checks at once.
