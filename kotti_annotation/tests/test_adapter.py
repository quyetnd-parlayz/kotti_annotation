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
        # adapter = config.registry.queryAdapter(root, IAnnotations)
        adapter = IAnnotations(root)
        assert isinstance(adapter, SQLAAnnotations)

    def test_sqlajson(self, db_session, root):

        root.annotations = {'4':{4:'four'}}
        # root = db_session.query(Node).filter(Node.parent_id == None).one()
        assert root.annotations['4'] == {4:'four'}

    def test_CRUD(self, db_session, root):

        from kotti_annotation.adapters import SQLAAnnotations
        from kotti.resources import Node
        from transaction import commit
        root = db_session.query(Node).filter(Node.parent_id == None).one()
        adapter = SQLAAnnotations(root)

        # Only string key is supported
        with raises(TypeError):
            adapter[1] = 'one'
        adapter['1'] = 'one'
        assert adapter['1'] == 'one'
        adapter['2'] = 2
        assert adapter['2'] == 2
        adapter['three'] = [1, '2', 3]
        assert adapter['three'] == [1, '2', 3]
        adapter['4'] = {4: 'four'}
        # import pdb; pdb.set_trace()
        assert adapter['4'] == {4: 'four'}
        adapter['4'] = 'five'
        assert adapter['4'] == 'five'
        assert '1' in adapter
        del adapter['1']
        with raises(KeyError):
            adapter['1']
