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
        adapter1 = config.registry.queryAdapter(root, IAnnotations)
        assert isinstance(adapter1, SQLAAnnotations)
        adapter2 = IAnnotations(root)
        assert isinstance(adapter2, SQLAAnnotations)
        # assert adapter1 is adapter2

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
        assert root._annotations['1'].value == 'one'
        assert adapter['1'] == 'one'
        assert adapter.get('1') == 'one'
        assert adapter.get('2', None) == None

        # Test edit
        adapter['1'] = 2
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['1'] == 2

        # Complicated data structure
        adapter['2'] = [1, '2', 3]
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['2'] == [1, '2', 3]

        adapter['3'] = {4: 'four'}
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['3'] == {'4': 'four'}

        # Other dict function
        assert len(adapter) == 3
        keys = adapter.keys()
        keys.sort()
        assert keys == ['1', '2', '3']

        # Check Mutability
        adapter['2'][1] = ['2', 2]
        adapter['3']['4'] = {'5': 'five'}
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['2'] == [1, ['2', 2], 3]
        assert adapter['3'] == {'4': {'5': 'five'}}

        # Check nested Mutability
        adapter['2'][1][0] = 2
        adapter['3']['4']['5'] = 5
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['2'] == [1, [2, 2], 3]
        assert adapter['3'] == {'4': {'5': 5}}

        # Delete
        assert '1' in adapter
        del adapter['1']
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        with raises(KeyError):
            adapter['1']
        with raises(KeyError):
            del adapter['4']

        # Check special type
        import datetime
        now = datetime.datetime.now()
        adapter['1'] = now
        commit()
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)
        assert adapter['1'] == now
