# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from zope import component, interface
from zope.annotation.interfaces import IAnnotations

from pyramid.compat import string_types

try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

from kotti import DBSession
from kotti.sqla import JsonType

from kotti_annotation import _
from kotti_annotation.interfaces import IFlexContent
from kotti_annotation.resources import Annotation


@interface.implementer(IAnnotations)
@component.adapter(IFlexContent)
class SQLAAnnotations(DictMixin):
    """Store annotation on ``annotations`` SQLA table
    """

    def __init__(self, context):
        self.obj = context

    def __bool__(self):
        return DBSession.query(Annotation).filter_by(
            node_id=self.obj.id).first() is not None

    __nonzero__ = __bool__

    def get(self, key, default=None):
        """See zope.annotation.interfaces.IAnnotations"""
        anno = DBSession.query(Annotation).filter_by(
            node_id=self.obj.id, name=key).first()
        if anno is None:
            return default
        return anno.value

    def __getitem__(self, key):
        anno = DBSession.query(Annotation).filter_by(
            node_id=self.obj.id, name=key).first()
        if anno is None:
            raise KeyError(key)
        return anno.value

    def keys(self):
        return [ anno.name for anno in DBSession.query(
            Annotation.name).filter_by(node_id=self.obj.id).all()]

    def __iter__(self):
        return iter(DBSession.query(
            Annotation).filter_by(node_id=self.obj.id).all())

    def __len__(self):
        return DBSession.query(
            Annotation.name).filter_by(node_id=self.obj.id).count()

    def __setitem__(self, key, value):
        """See zope.annotation.interfaces.IAnnotations"""
        # import pdb; pdb.set_trace()
        if not isinstance(key, string_types):
            raise TypeError("Only string key is supported")
        anno = DBSession.query(Annotation).filter_by(
            node_id=self.obj.id, name=key).first()
        if anno is None:
            anno = Annotation(self.obj.id, key, value)
            # import pdb; pdb.set_trace()
            DBSession.add(anno)
        else:
            anno.value = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        DBSession.query(Annotation).filter_by(
            node_id=self.obj.id, name=key).delete()

    def __contains__(self, key):
        return DBSession.query(Annotation).filter_by(
            node_id=self.obj.id, name=key).first() is not None
