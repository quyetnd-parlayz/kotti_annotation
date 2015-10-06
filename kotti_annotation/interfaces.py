# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from zope.annotation.interfaces import IAnnotatable
from kotti.interfaces import IContent


class IFlexContent(IContent, IAnnotatable):
    """FlexContent have ability to set/get foreign attributes 
       via Annotation Storage"""
