:mod:`greatwar` -- Django-based Great War site
====================================================

.. module:: greatwar

:mod:`greatwar` is a django site for the Great War, based on the eXist-db xml database.


Models
------

Because greatwar is an eXist/xml-based site, models are based on
:class:`eulcore.xmlmap.XmlObject` and make use of
:class:`eulcore.existdb.query.QuerySet` for easy access to sections of
TEI xml, and for search and retrieval within the eXist database.


Great War sections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: greatwar.poetry.models.PoetryBook
   :members:

.. autoclass:: greatwar.poetry.models.Poem
   :members:

.. autoclass:: greatwar.poetry.models.Poet
   :members:

   
Views
-----
.. automodule:: greatwar.poetry.views
   :members:
   
.. 
    NOTE: documentation for views with condition decorator is NOT currently
    working; even though the django code uses the functools.wraps as specified,
    the docstring is getting lost because of the decorator.


Custom Template Filters & Tags
------------------------------
.. automodule:: greatwar.poetry.templatetags.tei
   :members:

