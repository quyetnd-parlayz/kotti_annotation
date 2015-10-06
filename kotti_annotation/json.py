# -*- coding: utf-8 -*-

"""
Json serializer/desrializer 
bytes from Tryton code base: 
http://hg.tryton.org/trytond/file/7e29cd647fad/trytond/protocols/jsonrpc.py

>>> from kotti_annotation.json import JSONDecoder 
>>> from kotti_annotation.json import JSONEncoder 
>>> json.dumps(data, cls=JSONEncoder)
>>> json.loads(data, object_hook=JSONDecoder())

"""

import datetime
from decimal import Decimal
from pyramid.compat import json


class JSONDecoder(object):

    decoders = {}

    @classmethod
    def register(cls, klass, decoder):
        assert klass not in cls.decoders
        cls.decoders[klass] = decoder

    def __call__(self, dct):
        if dct.get('__class__') in self.decoders:
            return self.decoders[dct['__class__']](dct)
        return dct

JSONDecoder.register('datetime',
    lambda dct: datetime.datetime(dct['year'], dct['month'], dct['day'],
        dct['hour'], dct['minute'], dct['second'], dct['microsecond']))
JSONDecoder.register('date',
    lambda dct: datetime.date(dct['year'], dct['month'], dct['day']))
JSONDecoder.register('time',
    lambda dct: datetime.time(dct['hour'], dct['minute'], dct['second'],
        dct['microsecond']))
JSONDecoder.register('timedelta',
    lambda dct: datetime.timedelta(seconds=dct['seconds']))


def _bytes_decoder(dct):
    cast = bytearray if bytes == str else bytes
    return cast(base64.decodestring(dct['base64']))
JSONDecoder.register('bytes', _bytes_decoder)
JSONDecoder.register('Decimal', lambda dct: Decimal(dct['decimal']))


class JSONEncoder(json.JSONEncoder):

    serializers = {}

    def __init__(self, *args, **kwargs):
        super(JSONEncoder, self).__init__(*args, **kwargs)
        # Force to use our custom decimal with simplejson
        self.use_decimal = False

    @classmethod
    def register(cls, klass, encoder):
        assert klass not in cls.serializers
        cls.serializers[klass] = encoder

    def default(self, obj):
        marshaller = self.serializers.get(type(obj),
            super(JSONEncoder, self).default)
        return marshaller(obj)

JSONEncoder.register(datetime.datetime,
    lambda o: {
        '__class__': 'datetime',
        'year': o.year,
        'month': o.month,
        'day': o.day,
        'hour': o.hour,
        'minute': o.minute,
        'second': o.second,
        'microsecond': o.microsecond,
        })
JSONEncoder.register(datetime.date,
    lambda o: {
        '__class__': 'date',
        'year': o.year,
        'month': o.month,
        'day': o.day,
        })
JSONEncoder.register(datetime.time,
    lambda o: {
        '__class__': 'time',
        'hour': o.hour,
        'minute': o.minute,
        'second': o.second,
        'microsecond': o.microsecond,
        })
JSONEncoder.register(datetime.timedelta,
    lambda o: {
        '__class__': 'timedelta',
        'seconds': o.total_seconds(),
        })
_bytes_encoder = lambda o: {
    '__class__': 'bytes',
    'base64': base64.encodestring(o),
    }
JSONEncoder.register(bytes, _bytes_encoder)
JSONEncoder.register(bytearray, _bytes_encoder)
JSONEncoder.register(Decimal,
    lambda o: {
        '__class__': 'Decimal',
        'decimal': str(o),
        })

