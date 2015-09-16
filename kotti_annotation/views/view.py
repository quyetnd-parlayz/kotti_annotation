# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_annotation import _
from kotti_annotation.resources import CustomContent
from kotti_annotation.fanstatic import css_and_js
from kotti_annotation.views import BaseView


@view_defaults(context=CustomContent, permission='view')
class CustomContentViews(BaseView):
    """ Views for :class:`kotti_annotation.resources.CustomContent` """

    @view_config(name='view', permission='view',
                 renderer='kotti_annotation:templates/custom-content-default.pt')
    def default_view(self):
        """ Default view for :class:`kotti_annotation.resources.CustomContent`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }

    @view_config(name='alternative-view', permission='view',
                 renderer='kotti_annotation:templates/custom-content-alternative.pt')
    def alternative_view(self):
        """ Alternative view for :class:`kotti_annotation.resources.CustomContent`.
        This view requires the JS / CSS resources defined in
        :mod:`kotti_annotation.fanstatic`.

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        css_and_js.need()

        return {
            'foo': _(u'bar'),
        }
