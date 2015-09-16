# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from kotti.resources import File
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_annotation')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_annotation.kotti_configure

        to enable the ``kotti_annotation`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_annotation'
    settings['kotti.alembic_dirs'] += ' kotti_annotation:alembic'
    settings['kotti.available_types'] += ' kotti_annotation.resources.CustomContent'
    settings['kotti.fanstatic.view_needed'] += ' kotti_annotation.fanstatic.css_and_js'
    File.type_info.addable_to.append('CustomContent')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_annotation:locale')
    config.add_static_view('static-kotti_annotation', 'kotti_annotation:static')

    config.scan(__name__)
