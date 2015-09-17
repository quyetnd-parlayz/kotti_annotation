# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from sqlalchemy.orm import relation
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String

from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

from kotti import Base
from kotti.resources import Node
from kotti.resources import Content
from kotti.sqla import JsonType

from kotti_annotation import _
from kotti_annotation.interfaces import IFlexContent



class Annotation(Base):
    """Persistent class (SQLA) for annotation
    """

    #: Foreign key referencing :attr:`Node.id`
    #: (:class:`sqlalchemy.types.Integer`)
    node_id = Column(Integer, ForeignKey('nodes.id'), primary_key=True)
    #: Name of the annotation
    #: (:class:`sqlalchemy.types.String`)
    name = Column(String(50), primary_key=True)
    #: Annotation value
    #: (:class:`kotti.sqla.JsonType`)
    value = Column(JsonType)
    #: Relation that adds a ``node`` :func:`sqlalchemy.orm.backref`
    #: to :class:`~kotti_annotation.resources.Annotation` instances
    #: (:func:`sqlalchemy.orm.relationship`)
    node = relation(Node)

    def __repr__(self):
        return self.value
        # return u"<Annotation '{0}' of '{1}': {2}>".format(
        #     self.name, self.node.__repr__(), self.value)

    def __init__(self, node_id, name, value):
        self.node_id = node_id
        self.name = name
        self.value = value


class FlexContentMixin(object):
    """FlexContent have ability to set/get foreign attributes 
       via Annotation Storage"""

    implements(IFlexContent)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            super(FlexContent, self).__setattr__(name,value)
        else:
            IAnnotations(self)[name] = value

    def __getattr__(self, name):
        try:
            return super(FlexContent, self).__getattr__(name)
        except AttributeError:
            anno = IAnnotations(self)
            if not name in anno:
                raise AttributeError
            return anno[name]
