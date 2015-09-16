kotti_annotation
****************

This is an extension to Kotti that add zope.annotation support to your kotti resource.

|build status|_

What it does
============

- (SQLA) Create ``annotations`` table to store node annotations

- Add zope.annotation ``IAnnotations`` adapter

- Add new base class for contenttype: ``FlexContent`` that can store foreign attributes in annotation storage

- (TBD) Intergrate with ``kotti_es`` for indexing support

`Find out more about Kotti`_

Development happens at https://github.com/quyetnd-parlayz/kotti_annotation

.. |build status| image:: https://secure.travis-ci.org/quyetnd-parlayz/kotti_annotation.png?branch=master
.. _build status: http://travis-ci.org/quyetnd-parlayz/kotti_annotation
.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_annotation.kotti_configure

Database upgrade
================

If you are upgrading from a previous version you might have to migrate your
database.  The migration is performed with `alembic`_ and Kotti's console script
``kotti-migrate``. To migrate, run
``kotti-migrate upgrade --scripts=kotti_annotation:alembic``.

For integration of alembic in your environment please refer to the
`alembic documentation`_. If you have problems with the upgrade,
please create a new issue in the `tracker`_.

Development
===========

Contributions to kotti_annotation are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
.. _tracker: https://github.com/quyetnd-parlayz/kotti_annotation/issues
.. _Github repository: https://github.com/quyetnd-parlayz/kotti_annotation
