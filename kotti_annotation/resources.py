# -*- coding: utf-8 -*-

from sqlalchemy.orm import relation
from sqlalchemy.orm import backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

from kotti import Base
from kotti.resources import Node
from kotti.resources import Content

from kotti_annotation import _
from kotti_annotation.interfaces import IFlexContent
from kotti_annotation.sqla import JSONAlchemy


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
    value = Column(JSONAlchemy(Text))
    node = relation(Node, backref=backref(
            "_annotations", 
            collection_class=attribute_mapped_collection('name'),
            cascade="all, delete-orphan"
            )
        )

    def __repr__(self): # pragma: no cover
        return str(self.value)
        # return u"<Annotation '{0}' of '{1}': {2}>".format(
        #     self.name, self.node.__repr__(), self.value)

    def __init__(self, node_id, name, value):
        self.node_id = node_id
        self.name = name
        self.value = value

