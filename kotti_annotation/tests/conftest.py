# -*- coding: utf-8 -*-

"""
Created on 2015-09-16
:author: quyetnd (quyet@parlayz.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_annotation.resources
    kotti_annotation.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_annotation.kotti_configure'}
