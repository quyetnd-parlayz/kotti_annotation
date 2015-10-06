# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_annotation')


def kotti_configure(settings): # pragma: no cover
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_annotation.kotti_configure

        to enable the ``kotti_annotation`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_annotation'
    settings['kotti.alembic_dirs'] += ' kotti_annotation:alembic'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.include('pyramid_zcml')
    config.load_zcml('configure.zcml')
    
    config.scan(__name__)
