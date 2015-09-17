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
# from kotti.sqla import 

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
        self._annotations = dict([(ann.name, ann) for ann in 
            DBSession.query(Annotation).filter_by(node_id=self.obj.id)])

    def __bool__(self):
        return len(self._annotations) > 0

    __nonzero__ = __bool__

    def get(self, key, default=None):
        """See zope.annotation.interfaces.IAnnotations"""
        if key not in self._annotations:
            return default
        return self._annotations[key].value

    def __getitem__(self, key):
        if key not in self._annotations: 
            raise KeyError(key)
        return self._annotations[key].value

    def keys(self):
        return self._annotations.keys()

    def __iter__(self):
        return iter(self._annotations)

    def __len__(self):
        return len(self._annotations)

    def __setitem__(self, key, value):
        """See zope.annotation.interfaces.IAnnotations"""
        # import pdb; pdb.set_trace()
        if not isinstance(key, string_types):
            raise TypeError("Only string key is supported")
        if not key in self._annotations:
            anno = Annotation(self.obj.id, key, value)
            self._annotations[key] = anno
            DBSession.add(anno)
        else:
            self._annotations[key].value = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        if not key in self._annotations:
            return
        anno = self._annotations.pop(key)
        DBSession.delete(anno)

    def __contains__(self, key):
        return key in self._annotations
