# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from pytest import mark, raises


class TestAnnotation:

    def test_component_lookup(self, config, root):

        from kotti_annotation.adapters import SQLAAnnotations
        from kotti_annotation.interfaces import IFlexContent
        from zope.annotation.interfaces import IAnnotations
        from zope.interface import directlyProvides

        config.include('kotti_annotation')
        # Add IFlexContent interfaces to root
        directlyProvides(root, IFlexContent)
        # Adapter query
        adapter = config.registry.queryAdapter(root, IAnnotations)
        assert isinstance(adapter, SQLAAnnotations)
        adapter = IAnnotations(root)
        assert isinstance(adapter, SQLAAnnotations)

    def test_CRUD(self, db_session, root):

        from kotti_annotation.adapters import SQLAAnnotations
        from kotti.resources import Node
        from transaction import commit
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)

        assert not adapter

        # Only string key is supported
        with raises(TypeError):
            adapter[1] = 'one'

        # Check if data is persisted
        adapter['1'] = 'one'
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['1'] == 'one'

        adapter['2'] = 2
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['2'] == 2

        adapter['3'] = [1, '2', 3]
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['3'] == [1, '2', 3]

        adapter['4'] = {4: 'four'}
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['4'] == {'4': 'four'}
        assert len(adapter) == 4
        keys = adapter.keys()
        keys.sort()
        assert keys == ['1', '2', '3', '4']

        # Check Mutability
        adapter['4']['4'] = 'five'
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['4'] == {'4': 'five'}

        assert '1' in adapter
        del adapter['1']
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        with raises(KeyError):
            adapter['1']
